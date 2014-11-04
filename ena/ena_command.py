#!/usr/bin/env python

"""
Command line scraper delegator.

ena_scraper --state=MN --election=20141104 results
"""

import logging, os, sys, argparse



class ENACommand(object):
    """
    This is built as a command line tool and not meant for library inclusion.
    """

    description = """
examples:

  Update results for the 2014-11-04 election
  $ ena --state=MN --election=20141104 results

    """

    def __init__(self):
        """
        Constructor.
        """
        self.parser = argparse.ArgumentParser(
            description = self.description,
            formatter_class = argparse.RawDescriptionHelpFormatter)

        # State
        self.parser.add_argument(
            'state',
            help = 'The state to get data from.'
        )

        # Function
        self.parser.add_argument(
            'function',
            help = 'The function or method to call.'
        )

        # Bucket path
        self.parser.add_argument(
            '-e', '--election',
            dest = 'election',
            help = 'The election ID which should is most often a date like 20141104.  If not given, the newest election found will be used.',
            default = ''
        )

        # Turn on debugging
        self.parser.add_argument(
            '-d', '--debug',
            action = 'store_true',
            help = 'Turn on debugging.'
        )

        # Parse options
        self.args = self.parser.parse_args()

        # Debugging
        if self.args.debug:
            logging.basicConfig(level = logging.DEBUG)

        # Done
        self.out('- Done.\n')


    def out(self, message):
        """
        Wrapper around stdout
        """
        sys.stdout.write(message)


# Handle execution
if __name__ == '__main__':
    ena_command = ENACommand()
