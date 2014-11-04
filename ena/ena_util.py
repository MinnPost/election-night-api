#!/usr/bin/env python

"""
Utilities for scraping.
"""

import os, sys, json, calendar, datetime
import scraperwiki
from gdata.spreadsheet.service import SpreadsheetsService



class ENAUtils(object):
    """
    This class creates a set of methods for scraping.
    """

    # Where the scrapers are
    scraper_dir = os.path.join(os.path.dirname(__file__), '../states')
    # Where the sqlite db is
    db_file = os.path.join(os.path.dirname(__file__), '../scraperwiki.sqlite')
    # Whether to turn of synchronous on the database
    db_synchronous = False
    # Typing for google spreadsheets, maybe this should be done
    # with Pickle?
    google_spreadsheet_types = {
        'percentage': float,
        'votes_candidate': int,
        'ranked_choice_place': int,
        'percent_needed': float
    }


    def __init__(self, state, election, debug = False, db_file = False, logger = False):
        """
        Constructor.
        """
        self.state = state.lower()

        # Logging
        self.logger = self.default_logger if logger == False else logger

        # Get meta file
        self.meta_file = os.path.join(self.scraper_dir, state, '%s_meta.py' % self.state)
        if os.path.exists(self.meta_file) and os.path.isfile(self.meta_file):
            self.meta = __import__('states.%s.%s_meta' % (self.state, self.state),
                globals(), locals(), ['meta'], -1).meta

        # Determine election.  If not defined, we use the newest one
        if election in ['', None, False]:
            newest = datetime.date(1970, 1, 1)
            for m in self.meta:
                if self.meta[m]['date'] > newest:
                    self.election = self.meta[m]
        else:
            self.election = self.meta[election]

        # Overall, we shouldn't change the db, but for testing, it is
        # helpful
        if db_file not in ['', None, False]:
            self.db_file = db_file


    def setup(self):
        """
        Setup to run when initializing.  This should be run in your contructor.
        """
        # Scraperwiki's default db is relative to where the script
        # is running but be default the db is created at scraperwiki.sqlite
        # where you are, but this should be empty since we don't use it
        scraperwiki.sql._State.db_path = 'sqlite:///%s' % self.db_file

        # Make sure the DB is efficient.  Synchronous off means that power outage
        # or possible interruption can corrupt database
        if self.db_synchronous == False:
            scraperwiki.sql.execute('PRAGMA SYNCHRONOUS = OFF')
        scraperwiki.sql.execute('VACUUM')

        # Attach scraperwiki
        self.sql = scraperwiki.sql


    def default_logger(self, message):
        """
        Just a wrapper around print.
        """
        print message


    def timestamp(self):
        """
        Makes a timestamp.

        Returns:
        Int
        """
        return calendar.timegm(datetime.datetime.utcnow().utctimetuple())


    def save(self, ids, data, table, index_method = None):
        """
        Save a row to the database

        Arguments:
        ids - Array of fields that are identifiers, e.g. ['id']
        data - Array of, or a dictionary of data, for instance
            { 'id': 123, 'foo': 'bar' }
        table - String name of table to save to

        Keyword arguments:
        index_method - function to call to add an index to the table
            this will only be called once on a table.

        Returns:
        nothing
        """
        try:
            self.sql.save(unique_keys = ids, data = data, table_name = table)

            # Create index if needed
            if index_method is not None and callable(index_method) and not self.index_created[table]:
                index_method()
                self.index_created[table] = True
        except Exception, err:
            self.logger('Error thrown while saving to table %s, with data: %s' % (table, data))
            raise


    def save_meta(self, key, value):
        """
        Use this to save data about the election which will
        be available to the API.

        Since the scraperwiki-library changed to a binary blob to store
        the variables and the dumptruck-web code does not apprciate that,
        we get around it by making our own table.    This is not ideal,
        but faster than expecting to get changes pulled upstream.

        Arguments:
        key - String key
        value - The value to save

        Returns:
        nothing
        """

        # First determine if the table is already made, we need to be explicit
        # about column types
        table_query = "name FROM sqlite_master WHERE type='table' AND name='meta'"
        table_found = scraperwiki.sql.select(table_query)
        if table_query == []:
            create_table = u"CREATE TABLE IF NOT EXISTS %s (`key` text PRIMARY KEY, `value_blob` blob, `type` text)" % quote(self.__vars_table)
            scraperwiki.sql.execute(sql)

        # Then save the data we have
        self.save(['key'], {
            'key': key,
            'value': value,
            'type': type(value).__name__
        }, 'meta')


    def google_spreadsheet(self, spreadsheet_id, worksheet_id):
        """
        Get data from a Google spreadsheet.  Update self.google_spreadsheet_types
        to get type other data if needed.

        Arguments:
        spreadsheet_id - ID of spreadsheet, this is the long hash in the URL
        worksheet_id - The 0-based index of the sheets

        Returns:
        Array of rows of data
        """
        rows = []
        try:
            # We do some hackery to get the correct worksheet ID
            client = SpreadsheetsService()
            feed = client.GetWorksheetsFeed(spreadsheet_id, visibility='public', projection='basic')
            worksheet_id = feed.entry[worksheet_id].id.text.rsplit('/', 1)[1]
            rows = client.GetListFeed(key = spreadsheet_id, wksht_id = worksheet_id, visibility = 'public', projection = 'values').entry
        except Exception, err:
            self.logger('Unable to connect to supplemental source: %s, %s' % (spreadsheet_id, worksheet_id))

        # Process the rows into a more usable format.  And handle typing
        if len(rows) > 0:
            p_rows = []
            for r in rows:
                p_row = {}
                for f in r.custom:
                    # Try typing
                    c = f.replace('.', '_')
                    if r.custom[f].text is not None and c in self.google_spreadsheet_types:
                        p_row[c] = self.google_spreadsheet_types[c](r.custom[f].text)
                    else:
                        p_row[c] = r.custom[f].text

                p_rows.append(p_row)

            return p_rows

        return rows



    def index_results(self):
        """
        Make index for results table.
        """
        index_query = "CREATE INDEX IF NOT EXISTS %s ON results (%s)"
        scraperwiki.sql.execute(index_query % ('office_name', 'office_name'))
        scraperwiki.sql.execute(index_query % ('candidate', 'candidate'))
        scraperwiki.sql.execute(index_query % ('contest_id', 'contest_id'))


    def index_contests(self):
        """
        Make index for contests table.
        """
        index_query = "CREATE INDEX IF NOT EXISTS %s ON contests (%s)"
        scraperwiki.sql.execute(index_query % ('title', 'title'))
        scraperwiki.sql.execute(index_query % ('sub_title', 'sub_title'))
