#!/usr/bin/env python
"""
Main scraper for VA
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
        Scrape results

        This was developed for the VA results file from the November 4, 2014
        general election. Some updating may be necessary if file layout changes.
        """

        # Load and scrape the results file
        scraped = self.util.scrape(self.util.election['url'])

        rows = unicodecsv.reader(scraped.splitlines(), delimiter=',', quotechar='"', encoding='latin-1')

        #skip header row
        rows.next()

        contests = {}
        results = {}

        for row in rows:
            #Establish IDs
            contest_id = str(row[12])

            if contest_id not in contests:
                contests[contest_id] = {}

            #create unique id for precincts, to see which have already been counted
            precinct_id = row[4] + "-" + row[8]

            #test if precinct ID is already in list of precincts
            if 'all_precincts' in contests[contest_id]:
                if precinct_id not in contests[contest_id]['all_precincts'] and '###' not in precinct_id:
                    contests[contest_id]['all_precincts'].append(precinct_id)
            else:
                if '###' not in precinct_id:
                    contests[contest_id]['all_precincts'] = [precinct_id]

            #make separate list of precincts that actually have non-blank vote
            #totals (i.e. the precinct has reported) Precincts with ## are not
            #counted toward the total
            if 'counted_precincts' in contests[contest_id]:
                if precinct_id not in contests[contest_id]['counted_precincts'] and row[20] != '' and '###' not in precinct_id:
                    contests[contest_id]['counted_precincts'].append(precinct_id)
            else:
                if row[20] != '' and '###' not in precinct_id:
                    contests[contest_id]['counted_precincts'] = [precinct_id]

            #contest title
            if 'title' not in contests[contest_id]:
                contests[contest_id]['title'] = row[5]
                #add description for things with multiple districts, like US Rep
                if row[15] != 'Statewide':
                    contests[contest_id]['title'] += ' ' + row[15]

            #Treat ballot questions differently from candidates
            if row[11] == '':
                #ballot question handling
                choice_id = str(row[13])
                choice_idy = choice_id + 'y'
                choice_idn = choice_id + 'n'

                if choice_idy not in results:
                    results[choice_idy] = {}
                if choice_idn not in results:
                    results[choice_idn] = {}

                if 'contest_id' not in results[choice_idy]:
                    results[choice_idy]['contest_id'] = contest_id
                if 'contest_id' not in results[choice_idn]:
                    results[choice_idn]['contest_id'] = contest_id

                if 'choice' not in results[choice_idy]:
                    results[choice_idy]['choice'] = 'Yes'
                if 'choice' not in results[choice_idn]:
                    results[choice_idn]['choice'] = 'No'

                results[choice_idy]['party'] = ''
                results[choice_idn]['party'] = ''

                #add votes to result and to contest total
                yes_votes = int(row[20]) if row[20] != '' else 0
                no_votes = int(row[21]) if row[21] != '' else 0
                votes = yes_votes + no_votes

                if 'votes' in results[choice_idy]:
                    results[choice_idy]['votes'] += yes_votes
                else:
                    results[choice_idy]['votes'] = yes_votes

                if 'votes' in results[choice_idn]:
                    results[choice_idn]['votes'] += no_votes
                else:
                    results[choice_idn]['votes'] = no_votes

                if 'total_votes' in contests[contest_id]:
                    contests[contest_id]['total_votes'] += votes
                else:
                    contests[contest_id]['total_votes'] = votes

            else:
                #candidate handling
                choice_id = str(row[11])

                if choice_id not in results:
                    results[choice_id] = {}

                if 'contest_id' not in results[choice_id]:
                    results[choice_id]['contest_id'] = contest_id

                #Candidate names
                if 'choice' not in results[choice_id]:
                    results[choice_id]['choice'] = row[9]

                #Candidate parties
                if 'party' not in results[choice_id]:
                    results[choice_id]['party'] = row[17]

                #add votes to result and to contest total
                votes = int(row[20]) if row[20] != '' else 0

                if 'votes' in results[choice_id]:
                    results[choice_id]['votes'] += votes
                else:
                    results[choice_id]['votes'] = votes

                if 'total_votes' in contests[contest_id]:
                    contests[contest_id]['total_votes'] += votes
                else:
                    contests[contest_id]['total_votes'] = votes

        for choice_id in results:
            #calculate percentage for the candidate
            if 'total_votes' in contests[results[choice_id]['contest_id']]:
                percent = float(results[choice_id]['votes'])/float(contests[results[choice_id]['contest_id']]['total_votes'])
                percent = percent * 100
            else:
                percent = 0.0

            #figure out if we have a winner
            winner = False
            contest_id = results[choice_id]['contest_id']
            if contests[contest_id]['counted_precincts'] == contests[contest_id]['all_precincts']:
                this_votes = results[choice_id]['votes']
                other_votes = []
                for c in results:
                    if results[c]['contest_id'] == contest_id and c != choice_id:
                        other_votes.append(results[c]['votes'])

                winner = True
                for v in other_votes:
                    if v >= this_votes:
                        winner = False

            # Save some data
            self.util.save_results({
                'id': choice_id,
                'state': self.util.state,
                'election': self.util.election_id,
                'contest_id': results[choice_id]['contest_id'],
                'choice': results[choice_id]['choice'],
                'winner': winner,
                'party': results[choice_id]['party'],
                'votes': results[choice_id]['votes'],
                'percentage': percent,
                'updated': self.util.timestamp()
            });
        for contest_id in contests:
            #calculate the percent of precincts reporting
            percent = float(len(contests[contest_id]['counted_precincts']))/float(len(contests[contest_id]['all_precincts']))
            percent = percent * 100

            self.util.save_contests({
                'id': contest_id,
                'state': self.util.state,
                'election': self.util.election_id,
                'seats': 1,
                'title': contests[contest_id]['title'],
                'sub_title': '',
                'precincts_reporting': len(contests[contest_id]['counted_precincts']),
                'total_precincts': len(contests[contest_id]['all_precincts']),
                'percent_reporting': percent,
                'total_votes': contests[contest_id]['total_votes'],
                'updated': self.util.timestamp()
            });
