#!/usr/bin/env python

"""
Command line scraper delegator.

ena_scraper --state=MN --election=20141104 results
"""

import logging, os, sys, argparse
from datetime import datetime
from ena_util import ENAUtils



class ENACommand(object):
    """
    This is built as a command line tool and not meant for library inclusion.
    """

    description = """
examples:

  Update results for the 2014-11-04 election in MN
  $ ena MN --election=20141104 results

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

        # Function arguments
        self.parser.add_argument(
            '-a', '--args',
            dest = 'args',
            help = 'Any arguments to pass to the function',
            nargs = '+'
        )

        # Election
        self.parser.add_argument(
            '-e', '--election',
            dest = 'election',
            help = 'The election ID which is most often a date like 20141104.  If not given, the newest election found will be used.',
            default = ''
        )

        # Turn on debugging
        self.parser.add_argument(
            '-d', '--debug',
            dest = 'debug',
            action = 'store_true',
            help = 'Turn on debugging.'
        )

        # Turn on debugging
        self.parser.add_argument(
            '--remove-db',
            dest = 'remove_db',
            action = 'store_true',
            help = 'Remove the database before running scraper.  This is helpful for development and should not be used for production.'
        )

        # Parse options
        self.args = self.parser.parse_args()

        # Debugging
        if self.args.debug:
            logging.basicConfig(level = logging.DEBUG)

        # Remove database
        if self.args.remove_db and os.path.exists(util.db_file):
            self.out('Removing DB. \n')
            os.remove(util.db_file)

        # Run
        self.run(self.args.state, self.args.election, self.args.function, self.args.args, self.args.debug)


    def run(self, state, election, function, arguments = [], debug = False):
        """
        Run the method for a given state.  Abstracted so that this
        can be run via Python directly.
        """
        # Load up utility
        util = ENAUtils(state, election, debug)

        # Create scraper instance
        scraper = util.Scraper(util)

        # Call method
        method = getattr(scraper, function, None)
        if method and callable(method):
            # Time it
            start = datetime.now()
            self.out('Running %s scraper for %s ... ' % (function, state))

            # Run
            method(*arguments if arguments is not None else [])

            # How much time passed
            end = datetime.now() - start
            self.out('Done (in %.2f min). \n' % (round(float(end.seconds) / 60, 2)))
        else:
            raise Exception('Method %s not found in %s scraper.' % (function, state))


    def out(self, message):
        """
        Wrapper around stdout
        """
        sys.stdout.write(message)
        sys.stdout.flush()


# Handle execution
if __name__ == '__main__':
    ena_command = ENACommand()
