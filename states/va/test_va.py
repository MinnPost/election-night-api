#!/usr/bin/env python

"""
Tests to run through py.test
http://pytest.org/

Tests for VA
"""

import os
from ena import ena_util

# Import your state
# import mn
import va


# Test DB.
db_file = os.path.join(os.path.dirname(__file__), '../../tests/tests-scraperwiki.sqlite')


def create_scraper(election = False):
    """
    Wrapper to create instance of VA scraper.
    """
    if os.path.exists(db_file):
        os.remove(db_file)

    # Create util and scraper instance
    util = ena_util.ENAUtils('VA', election, True, db_file = db_file)
    return va.Scraper(util)


def test_meta():
    """
    Just get check the meta data is there.
    """
    scraper = create_scraper()
    assert type(scraper.util.meta) == dict
