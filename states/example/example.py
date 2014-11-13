#!/usr/bin/env python

"""
This is an example scraper.  You should update instaces of 'example' with the
state you are working on.

This is the main scraper for this state.  It needs to have a class called
Scraper.  The constructor for the class should take in an object which
will be an instance of the utility object.  Make sure to the run the
following in the constructor.

    utility.setup()

Manage election specific configuration in example_meta.py.  You can access
all the meta data as:

    utility.meta

You can access the current running election meta data from

    utility.election

The command line will create an instance of Scraper and the arbitrary method
will be called.
"""

import sys
import os
import re
import unicodecsv


class Scraper(object):
    """
    Class for Scraper.  This will be instantiated with the command line
    utility and will be passed the ENA utility object.
    """

    def __init__(self, utility):
        """
        Constructor for scraper.
        """
        self.util = utility

        # Make sure this is done before saving as this connects
        # to the right database
        self.util.setup()


    def results(self, *args):
        """
        Scrape results data.  Though the name of the method is arbitrary, this
        is a command name for the method that needs to be updated most
        often on election night.

        The data for states varies wildly and the following is just some
        example code and may not fit your needs at all.
        """

        # You can get a URL with something like
        scraped = sql.util.scrape(self.util.election.data_file)

        # You can also parse a CSV if that is the format it comes in with
        rows = unicodecsv.reader(scraped.splitlines(), delimiter=';', quotechar='|', encoding='latin-1')

        # You can then go through rows like this and save the results
        # and information about contests
        for row in rows:

            # Save results data
            self.util.save_results({
                'id': 123,
                'state': self.util.state,
                'election': self.util.election_id,
                'updated': self.util.timestamp(),
                'choice': row[7].replace('WRITE-IN**', 'WRITE-IN'),
                'contest_id': 112233,
                'party': row[10],
                'votes': int(row[13]),
                'percentage': float(row[14]),
                'winner': False
            })

            # Save contests data
            self.util.save_contests({
                'id': 112233,
                'state': self.util.state,
                'election': self.util.election_id,
                'updated': self.util.timestamp(),
                'title': row[4],
                'precincts_reporting': int(row[11]),
                'total_precincts': int(row[12]),
                'percent_reporting': float(row[11]) / float(row[12]),
                'total_votes': int(row[15]),
                'seats': 1,
                'primary': self.util.election['primary'] if 'primary' in self.util.election else False
            })
