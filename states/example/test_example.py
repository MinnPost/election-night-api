#!/usr/bin/env python

"""
Tests to run through py.test
http://pytest.org/

This is an example set of tests to run.  Update places where you see
'example' with the state you are working on.
"""

import os
from ena import ena_util

# Import your state
# import mn
import example


# Test DB.
db_file = os.path.join(os.path.dirname(__file__), '../../tests/tests-scraperwiki.sqlite')


def create_scraper(election = False):
    """
    Wrapper to create instance of Example scraper.
    """
    if os.path.exists(db_file):
        os.remove(db_file)

    # Create util and scraper instance
    util = ena_util.ENAUtils('example', election, True, db_file = db_file)
    return example.Scraper(util)


def test_meta():
    """
    Just get check the meta data is there.
    """
    scraper = create_scraper()
    assert type(scraper.util.meta) == dict
