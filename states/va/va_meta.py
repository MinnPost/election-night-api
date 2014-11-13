#!/usr/bin/env python

"""
Meta data for the VA elections.
"""

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
        'primary': False

        #...

    }
}
