#!/usr/bin/env python

"""
Meta data for the MN elections.
"""

from datetime import date


# The name of the variable is important.  Each entry entry in the dict
# is for an election.  The key is arbitrary but will be used by the
# command line to scrape a specific election
meta = {
    # Eleciton ID
    '20141104': {
        # Date of election
        'date': date(2014, 11, 04)

    }
}
