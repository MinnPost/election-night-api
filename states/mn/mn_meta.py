#!/usr/bin/env python

'''
Meta data for the MN elections.
'''

from datetime import date


# The name of the variable is important.  Each entry in the dict
# is for an election.  The key is arbitrary but will be used by the
# command line to scrape a specific election.  The utility tool will try
# to use the newest election ID so YYYYMMDD is suggested.
meta = {
    # Eleciton ID
    '20141104': {
        # Date of election
        'date': date(2014, 11, 04),
        # Whether primary
        'primary': False,

        # The following are not required

        # Base URL of files
        'base_url': 'ftp://media:results@ftp.sos.state.mn.us/20141104/',
        # Refernece to formates
        'layout': 'http://electionresults.sos.state.mn.us/Select/DownloadFileFormats/20',

        # Set of results to get data from
        'results': {
            'us_house_results': {
                'url': 'ushouse.txt',
                'scope': 'us_house'
            },
            'us_senate_results': {
                'url': 'ussenate.txt',
                'scope': 'state'
            },
            'attorney_general_results': {
                'url': 'attorneygen.txt',
                'scope': 'state'
            },
            'auditor_results': {
                'url': 'auditor.txt',
                'scope': 'state'
            },
            'governor_results': {
                'url': 'Governor.txt',
                'scope': 'state'
            },
            'secretary_results': {
                'url': 'secofstate.txt',
                'scope': 'state'
            },
            'state_house_results': {
                'url': 'LegislativeByDistrict.txt',
                'scope': 'state_house'
            },
            'judicial_results': {
                'url': 'judicial.txt',
                'scope': 'state'
            },
            'judicial_district_results': {
                'url': 'judicialdst.txt',
                'scope': 'district_court'
            },
            'county_results': {
                'url': 'cntyRaceQuestions.txt',
                'scope': 'county'
            },
            # Includes both municpal questions (cityquestions.txt) and candidate results.
            'municipal_results': {
                'url': 'local.txt',
                'scope': 'municipal'
            },
            # Includes both school questions (SchoolQuestions.txt) and candidate results.
            'school_district_results': {
                'url': 'sdraceQuesions.txt',
                'scope': 'school'
            },
            'hospital_results': {
                'url': 'hospital.txt',
                'scope': 'hospital'
            }
        },
        # Set of reference table that we can use later if needed
        'references': {
            'parties': {
                'url': 'PartyTbl.txt',
                'table': 'parties',
                'type': 'parties'
            },
            'candidates': {
                'url': 'cand.txt',
                'table': 'candidates',
                'type': 'candidates'
            },
            'local_candidates': {
                'url': 'LocalCandTbl.txt',
                'table': 'candidates',
                'type': 'local_candidates'
            }
        },
        # Areas that can be used for boundary matching later
        'areas': {
            'counties': {
                'url': 'Cntytbl.txt'
            },
            'municipalities': {
                'url': 'MunTbl.txt'
            },
            'precincts': {
                'url': 'PrctTbl.txt'
            },
            'school_districts': {
                'url': 'SchoolDistTbl.txt'
            }
        },
        # Question body
        'questions': {
            'ballot_questions': {
                'url': 'BallotQuestions.txt'
            }
        },
        # Supplementable results via Google spreadsheets
        'supplements': {
            'contests': {
                'spreadsheet_id': '1f3uc7P-WEeqJPkIlN14lhtGghRyIVsV08k6QISi2JNs',
                # Workesheet ID is the zero-based ID from the order of workssheets
                # and is used to find the actual ID
                'worksheet_id': 0
            }
        }
    }
}
