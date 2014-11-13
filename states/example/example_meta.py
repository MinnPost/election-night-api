#!/usr/bin/env python

"""
Metadata for the state.  This is just a configuration file.  Putting
in information about specifics that change from each election will
help the election scraper be more generic.

The name of the "meta" variable is important.  Each entry in the dict
is for an election.  The key is arbitrary but will be used by the
command line to scrape a specific election.  The utility tool will try
to use the newest election ID so YYYYMMDD is suggested.
"""

from datetime import date


# The name of the variable is important!
meta = {
    # Election ID
    '20141104': {
        # Date of election (required)
        'date': date(2014, 11, 4),
        # Whether primary (required, though this is used how you see fit)
        'primary': False,

        # The following are not required
        'data_file': 'http://electionresults.sos.state.mn.us/Results/MediaResult/20?mediafileid=56'
    },
    '20140812': {
        'date': date(2013, 8, 12),
        'primary': True,
        'data_file': 'http://minnesotaelectionresults.sos.state.mn.us/Results/MediaResult/19?mediafileid=35'
    }
}
