#!/bin/sh

# This wrapper will run the ENA scraper tool, but first check that it is
# not running elsewhere.  In conjunction with cron, this will allow
# a scraper to run continuously.
#
# This wrapper will pass arguments through to the ENA scraper tool.
#
# For instance:
# * * * * * $ENA_PATH/bin/ena MN results

# Ensure we have ENA PATH
if [ -z "$ENA_PATH" ]; then
    echo "Need to set ENA_PATH to the directory where the Election Night API code is"
    exit 1
fi

# Some helpful vars
ENA_COMMAND=$ENA_PATH/bin/ena

# Only run if not running
if ps -ef | grep -v grep | grep python.*ena ; then
    exit 0
else
    # Pass arguments through
    $ENA_COMMAND "$@"
fi
