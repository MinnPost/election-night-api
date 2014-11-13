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
        rows = self.util.scrape('https://voterinfo.sbe.virginia.gov/PublicSite/Public/results/Nov2014General.txt')

        for row in rows:

            #Determine if candidate or ballot question -- ID in different column
            if row[11] != '':


            # Save some data (Example)
            self.util.save_results({
                'id': 'test-row',
                'state': self.util.state,
                'election': self.util.election_id,
                'contest_id': row[12],
                'candidate': row[9], #if actual candidate - blank if ballot q
                'incumbent': False,
                'party': row[17],
                'votes': row[20],
                #'percentage': 25.0, Percentage not calculated
                'updated': self.util.timestamp()
            });
            self.util.save_contests({
                'id': row[12],
                'state': self.util.state,
                'election': self.util.election_id,
                'title': str(row[5]) + ' ' + str(row[15]) if row[15] != 'Statewide' else row[5],
                'sub_title': '',
                'precincts_reporting': 10, #going to have to calculate this
                'total_precincts': 100, #also going to have to calculate this
                'percent_reporting': 10.0, #and calculate this
                'total_votes': row[20],
                'updated': self.util.timestamp()
            });
