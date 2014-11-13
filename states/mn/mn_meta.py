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

        # Base URL of files.  FTP has traditionally been more stable, but that
        # is no longer always true
        'base_ftp': 'ftp://media:results@ftp.sos.state.mn.us/20141104/%s',
        'base_http': 'http://electionresults.sos.state.mn.us/Results/MediaResult/20?mediafileid=%s',

        # HTTP download list
        # http://electionresults.sos.state.mn.us/Select/Download/20
        # Refernece to formats
        # http://electionresults.sos.state.mn.us/Select/DownloadFileFormats/20

        # Set of results to get data from
        'results': {
            'us_house_results': {
                'ftp_file': 'ushouse.txt',
                'http_file': '24',
                'scope': 'us_house'
            },
            'us_senate_results': {
                'ftp_file': 'ussenate.txt',
                'http_file': '41',
                'scope': 'state'
            },
            'attorney_general_results': {
                'ftp_file': 'attorneygen.txt',
                'http_file': '35',
                'scope': 'state'
            },
            'auditor_results': {
                'ftp_file': 'auditor.txt',
                'http_file': '36',
                'scope': 'state'
            },
            'governor_results': {
                'ftp_file': 'Governor.txt',
                'http_file': '56',
                'scope': 'state'
            },
            'secretary_results': {
                'ftp_file': 'secofstate.txt',
                'http_file': '34',
                'scope': 'state'
            },
            'state_house_results': {
                'ftp_file': 'LegislativeByDistrict.txt',
                'http_file': '20',
                'scope': 'state_house'
            },
            'judicial_results': {
                'ftp_file': 'judicial.txt',
                'http_file': '37',
                'scope': 'state'
            },
            'judicial_district_results': {
                'ftp_file': 'judicialdst.txt',
                'http_file': '44',
                'scope': 'district_court'
            },
            'county_results': {
                'ftp_file': 'cntyRaceQuestions.txt',
                'http_file': '88',
                'scope': 'county'
            },
            # Includes both municpal questions (cityquestions.txt) and candidate results.
            'municipal_results': {
                'ftp_file': 'local.txt',
                'http_file': '1',
                'scope': 'municipal'
            },
            # Includes both school questions (SchoolQuestions.txt) and candidate results.
            'school_district_results': {
                'ftp_file': 'sdraceQuesions.txt',
                'http_file': '7',
                'scope': 'school'
            },
            'hospital_results': {
                'ftp_file': 'hospital.txt',
                'http_file': '90',
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
