#!/usr/bin/env python
"""
Main scraper for VA
"""

import sys
import os
import re
import unicodecsv
import datetime
import calendar
import json
import requests
import lxml.html


class Scraper:
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
        Scrape results

        Called with command like like:
        ena VA results
        """

        # Scrape
        #scraped = self.util.scrape('https://voterinfo.sbe.virginia.gov/PublicSite/Public/results/Nov2014General.txt')
        scraped = self.util.scrape('file:///Users/tomnehil/Desktop/Nov2014General.csv')

        rows = unicodecsv.reader(scraped.splitlines(), delimiter=',', quotechar='"', encoding='latin-1')

        rows.next()

        for row in rows:

            #Determine if candidate or ballot question -- ID in different column
            if row[11] != '':
                choice_id = str(row[11])
            else:
                choice_id = str(row[13])

            votes = int(row[20]) if row[20] != '' else 0
            contest_votes_total = votes

            if self.util.has_table('results') and self.util.has_table('contests'):

                #Read current vote total for this result row
                result_votes = self.util.sql.select("* from results where id='%s'" % choice_id)
                if result_votes != []:
                    votes += result_votes[0]['votes']

                #Also read current vote total for contest overall
                contest_votes = self.util.sql.select("* from contests where id='%s'" % row[12])
                if contest_votes != []:
                    contest_votes_total += contest_votes[0]['total_votes']

            #Precinct handling. The file is by precinct, so we need to total
            #these up for contests table.

            # Save some data (Example)
            self.util.save_results({
                'id': choice_id,
                'state': self.util.state,
                'election': self.util.election_id,
                'contest_id': row[12],
                'choice': row[9] if row[9] != '' else row[6], #9 is cand. name, 6 is ballot q
                'winner': False,
                'party': row[17],
                'votes': votes,
                'percentage': float(votes)/float(contest_votes_total) if contest_votes_total != 0 else 0.0,
                'updated': self.util.timestamp()
            });
            self.util.save_contests({
                'id': row[12],
                'state': self.util.state,
                'election': self.util.election_id,
                'title': row[5] + ' ' + row[15] if row[15] != 'Statewide' else row[5],
                'sub_title': '',
                'precincts_reporting': 10, #going to have to calculate this
                'total_precincts': 100, #also going to have to calculate this
                'percent_reporting': 10.0, #and calculate this
                'total_votes': contest_votes_total,
                'updated': self.util.timestamp()
            });
