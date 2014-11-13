#!/usr/bin/env python
"""
Main scraper for MN
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
        ena MN results
        """

        # Scrape (Example)
        self.util.scrape('http://google.com')

        # Save some data (Example)
        self.util.save_results({
            'id': 'test-row',
            'state': self.util.state,
            'election': self.util.election_id,
            'contest_id': 'contest-test-id',
            'candidate': 'Candidate Name',
            'incumbent': False,
            'party': 'R',
            'votes': 10,
            'percentage': 25.0,
            'updated': self.util.timestamp()
        });
        self.util.save_contests({
            'id': 'test-row',
            'state': self.util.state,
            'election': self.util.election_id,
            'title': 'Contest Race',
            'sub_title': '',
            'precincts_reporting': 10,
            'total_precincts': 100,
            'percent_reporting': 10.0,
            'total_votes': 1111,
            'updated': self.util.timestamp()
        });
