#!/usr/bin/env python

"""
Tests to run through py.test
http://pytest.org/
"""

import os
from ena import ena_util

# Test DB
db_file = os.path.join(os.path.dirname(__file__), './scraperwiki-test.sqlite')
if os.path.exists(db_file):
    os.remove(db_file)


def test_instantiation():
    """
    Just test basic instationation.
    """
    ena_util_in = ena_util.ENAUtils('MN', '20141104', debug = True, db_file = db_file)
    assert isinstance(ena_util_in, ena_util.ENAUtils)

def test_newest_election():
    """
    Use newest election
    """
    ena_util_in = ena_util.ENAUtils('MN', False, debug = True, db_file = db_file)
    assert type(ena_util_in.election) == dict

def test_setup():
    """
    Test setup
    """
    ena_util_in = ena_util.ENAUtils('MN', False, debug = True, db_file = db_file)
    ena_util_in.setup();
    assert os.path.exists(ena_util_in.db_file) and os.path.isfile(ena_util_in.db_file)

def test_timestamp():
    """
    Test timestamp.
    """
    ena_util_in = ena_util.ENAUtils('MN', False, debug = True, db_file = db_file)
    ts = ena_util_in.timestamp();
    assert type(ts) == int and ts > 0

def test_save():
    """
    Test a save.
    """
    ena_util_in = ena_util.ENAUtils('MN', False, debug = True, db_file = db_file)
    ena_util_in.setup();
    ena_util_in.save(['id'], { 'id': 123, 'foo': 'bar' }, 'test');
    rows = ena_util_in.sql.select('* FROM test')
    assert rows != [] and rows[0]['foo'] == 'bar'

def test_save_meta():
    """
    Test a save.
    """
    ena_util_in = ena_util.ENAUtils('MN', False, debug = True, db_file = db_file)
    ena_util_in.setup();
    ena_util_in.save_meta('test', 1234);
    rows = ena_util_in.sql.select('* FROM meta')
    assert rows != []

def test_google_spreadsheet():
    """
    Test a save.
    """
    ena_util_in = ena_util.ENAUtils('MN', False, debug = True, db_file = db_file)
    ena_util_in.setup();
    rows = ena_util_in.google_spreadsheet('1f3uc7P-WEeqJPkIlN14lhtGghRyIVsV08k6QISi2JNs', 0);
    assert rows != []
