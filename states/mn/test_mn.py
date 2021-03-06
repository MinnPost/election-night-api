#!/usr/bin/env python

"""
Tests to run through py.test
http://pytest.org/
"""

import os
from ena import ena_util
import mn

# Test DB.
db_file = os.path.join(os.path.dirname(__file__), '../../tests/test-scraperwiki.sqlite')


def create_scraper(election = False):
    """
    Wrapper to create instance of MN scraper.
    """
    # Remove DB if there
    if os.path.exists(db_file):
        os.remove(db_file)

    # Create util and scraper instance
    util = ena_util.ENAUtils('MN', election, True, db_file = db_file)
    return mn.Scraper(util)


def test_meta():
    """
    Just get check the meta data is there.
    """
    scraper = create_scraper()
    assert type(scraper.util.meta) == dict
