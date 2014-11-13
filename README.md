# Election Night API

A set of scrapers to create an API for election night applications.  This is aimed at small to medium orgs that cannot afford services like AP or Reuters elections, or orgs that need more local results.  This is also aimed at state-level results and for states that have some sort of election night live feed.

## Development (and install)

### Prerequisites

You may have the following already installed.

1. Install [Git](http://git-scm.com/).
1. Install [Python](https://www.python.org/downloads/).
    * Most systems already have Python installed.
1. Install [libxml](http://xmlsoft.org/).
    * On Mac, this should be installed with XCode developer tools: `xcode-select --install`
1. (optional) Use [virtualenv](http://virtualenv.readthedocs.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
    1. `pip install virtualenv virtualenvwrapper`
        * This may need to be run with `sudo`; you should be able to tell if you get a permission error.

### Get code and install dependencies

1. Get the code and change to directory: `git clone https://github.com/MinnPost/election-night-api.git && cd election-night-api`
1. (optional) Make a virtualenv to work in: `mkvirtualenv election-night-api`
1. Install libraries: `pip install -r requirements.txt`

## Tests

1. Run tests with: `py.test`

## Running

The `bin/ena` command is a wrapper to run each state scraper methods.  It is arbitrary what method to run, as the need to run certain methods on certain schedules can change from state to state.

* Get help on command: `bin/ena -h`
* Update results for the newest election in MN: `bin/ena MN results`
* Update areas data for specific election in MN: `bin/ana MN areas -e 20141104`
