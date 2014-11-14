#!/usr/bin/env python

"""
This is the example for when deploying for ScraperWiki.  See the README
for full instructions for deploying on ScraperWiki.
"""

SCRAPERWIKI_PLATFORM = True
import os, sys, json, calendar, datetime

# Get ena library
ena_path = os.path.join(os.path.dirname(__file__), '../election-night-api/ena')
if not os.path.exists(ena_path):
    print 'Election Night API not found'
    sys.exit(1)

sys.path.append(ena_path)
from ena_command import ENACommand

# Make command object
ena = ENACommand()

# Run commands here.  This is meant to run during off sesason (not around or on election
# night) so there is not reason to run thing very often.  Don't forget to set the
# schedule.
#
# The run command takes arguments: state, election, function, arguments, debug

###
# MANGE COMMAND HERE
###

# Minnesota (recent election) example
#ena.run('MN', None, 'questions')
#ena.run('MN', None, 'areas')
#ena.run('MN', None, 'results')

# Virginia (recent election) example
#ena.run('VA', None, 'results')
