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
        Scrape results data.  This should be made more efficient since it
        will be the one run most often.

        Called with command line like:
        ena MN results
        """

        # Go through and get the results data from each file
        for r in self.util.election['results']:
            result_set = self.util.election['results'][r]
            #url = self.util.election['base_ftp'] % (result_set['ftp_file'])

            url = self.util.election['base_http'] % (result_set['http_file'])

            try:
                scraped = self.util.scrape(url)
                # latin-1 is to support the occasional accent character
                rows = unicodecsv.reader(scraped.splitlines(), delimiter=';', quotechar='|', encoding='latin-1')
            except Exception, err:
                print 'Issue reading in results %s: %s' % (r, url)
                raise

            # Go through each row in the dataset
            for row in rows:
                # Create ids.
                # id-State-County-Precinct-District-Office
                base_id = 'id-' + row[0] + '-' + row[1] + '-' + row[2] + '-' + row[5] + '-' + row[3]
                # id-BASE-Candidate
                row_id = base_id + '-' + row[6]

                # Office refers to office name and office id as assigned by SoS, but
                # contest ID is a more specific id as office id's are not unique across
                # all results
                contest_id = base_id
                office_id = row[3]

                # Result record
                results_record = {
                    'id': row_id,
                    'state': self.util.state,
                    'election': self.util.election_id,
                    'updated': self.util.timestamp(),
                    'choice': row[7].replace('WRITE-IN**', 'WRITE-IN'),
                    'contest_id': contest_id,
                    'party': row[10],
                    'votes': int(row[13]),
                    'percentage': float(row[14]),
                    'winner': False # Calculate
                }

                # Contest record
                # The only way to know if there are multiple seats is look at the office
                # name which has "(Elect X)" in it.
                re_seats = re.compile('.*\(elect ([0-9]+)\).*', re.IGNORECASE)
                matched_seats = re_seats.match(row[4])

                # Primary is not designated in anyway, but we can make some initial
                # guesses. All contests in an election are considered primary, but
                # non-partisan ones only mean there is more than one seat available.
                is_primary = self.util.election['primary'] if 'primary' in self.util.election else False
                re_question = re.compile('.*\question.*', re.IGNORECASE)
                matched_question = re_question.match(row[4])
                is_primary = False if matched_question is not None else is_primary

                contests_record = {
                    'id': contest_id,
                    'state': self.util.state,
                    'election': self.util.election_id,
                    'updated': self.util.timestamp(),
                    'title': row[4],
                    'precincts_reporting': int(row[11]),
                    'total_precincts': int(row[12]),
                    'percent_reporting': float(row[11]) / float(row[12]),
                    'total_votes': int(row[15]),
                    'seats': int(matched_seats.group(1)) if matched_seats is not None else 1,
                    'primary': is_primary,

                    # Extra data
                    'scope': result_set['scope'],
                    'office_id': office_id,
                    'office_name': row[4],
                    'district_code': row[5],
                    'county_id': row[1],
                    'precinct_id': row[2]
                }

                # Save data found
                self.util.save_results(results_record)
                self.util.save_contests(contests_record)



    def areas(self, *args):
        """
        Scrape area meta data.  This does not need to be run often.

        Called with command line like:
        ena MN meta
        """

        # Go through and get the areas data
        for r in self.util.election['areas']:
            result_set = self.util.election['areas'][r]
            #url = self.util.election['base_ftp'] % (result_set['ftp_file'])

            url = self.util.election['base_http'] % (result_set['http_file'])

            try:
                scraped = self.util.scrape(url)
                # latin-1 is to support the occasional accent character
                rows = unicodecsv.reader(scraped.splitlines(), delimiter=';', quotechar='|', encoding='latin-1')
            except Exception, err:
                print 'Issue reading in area %s: %s' % (r, url)
                raise

            # Go through rows found
            for row in rows:

                # General data
                parsed = {
                    'id': r + '-',
                    'areas_group': r,
                    'county_id': None,
                    'county_name': None,
                    'ward_id': None,
                    'precinct_id': None,
                    'precinct_name': '',
                    'state_senate_id': None,
                    'state_house_id': None,
                    'county_commissioner_id': None,
                    'district_court_id': None,
                    'soil_water_id': None,
                    'school_district_id': None,
                    'school_district_name': '',
                    'mcd_id': None,
                    'precincts': None,
                    'name': '',
                    'updated': self.util.timestamp()
                }

                if r == 'municipalities':
                    parsed['id'] =    parsed['id'] + row[0] + '-' + row[2]
                    parsed['county_id'] = row[0]
                    parsed['county_name'] = row[1]
                    parsed['mcd_id'] = row[2]
                    parsed['name'] = row[1]

                if r == 'counties':
                    parsed['id'] =    parsed['id'] + row[0]
                    parsed['county_id'] = row[0]
                    parsed['county_name'] = row[1]
                    parsed['precincts'] = row[2]

                if r == 'precincts':
                    parsed['id'] =    parsed['id'] + row[0] + '-' + row[1]
                    parsed['county_id'] = row[0]
                    parsed['precinct_id'] = row[1]
                    parsed['precinct_name'] = row[2]
                    parsed['state_senate_id'] = row[3]
                    parsed['state_house_id'] = row[4]
                    parsed['county_commissioner_id'] = row[5]
                    parsed['district_court_id'] = row[6]
                    parsed['soil_water_id'] = row[7]
                    parsed['mcd_id'] = row[8]

                if r == 'school_districts':
                    parsed['id'] =    parsed['id'] + row[0]
                    parsed['school_district_id'] = row[0]
                    parsed['school_district_name'] = row[1]
                    parsed['county_id'] = row[2]
                    parsed['county_name'] = row[3]

                # Save final
                self.util.save(['id'], parsed, 'mn_areas')
