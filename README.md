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

### Tests

`py.test` will find all python files with [specific names](http://pytest.org/latest/goodpractises.html#test-discovery) in a given directory.

1. Run all the tests (including all the states): `py.test`
1. Run all the state tests: `py.test states/`
1. Run a specific state test: `py.test states/mn/`

## Running

The `bin/ena` command is a wrapper to run each state scraper methods.  It is arbitrary what method to run, as the need to run certain methods on certain schedules can change from state to state.

* Get help on command: `bin/ena -h`
* Update results for the newest election in MN: `bin/ena MN results`
* Update areas data for specific election in MN: `bin/ana MN areas -e 20141104`

## Data modeling

This tool allows you to model your data however you want for the most part, but there are some basic requirements.

### Contests

Contests are the generic word for races, ballot questions, referendums, etc.  This data should have at least the following fields, but you can have as many more fields as you want.

* `id`: A unique ID for the contest across the state and election
* `state`: State code, can be provided with `self.util.state`
* `election`: Election ID, can be provided with `self.util.election_id`
* `updated`: Timestamp integer of last updated, can use `self.util.timestamp()`
* `title`: Title of contest
* `precincts_reporting`: Integer number of precincts reporting
* `total_precincts`: Interger number of total precincts effected by contest
* `percent_reporting`: Float percentage (85.0, not 0.85) of precincts reporting
* `total_votes`: Integer of total votes cast
* `seats`: Seats available for contest, usually 1
* ... and whatever other data is relevant for this contest

The utility object has a convenient `save_contests` method for updating results.

### Results

Results are data for each candidate, write-in, answer, etc for each contests.  So there will be (probably) at least two rows of results per contest.

* `id`: A unique ID for the contest across the state and election.
* `state`: State code, can be provided with `self.util.state`
* `election`: Election ID, can be provided with `self.util.election_id`
* `updated`: Timestamp integer of last updated, can use `self.util.timestamp()`
* `contest_id`: The corresponding contest ID from the contests table
* `choice`: The name of the candidate or question answer (Yes or No usually)
* `party`: Party identifier, such as `D` or `R`
* `votes`: Integer number of votes this choice recieved
* `percentage`: Float percentage (85.0, not 0.85) of the number of votes recieved in contest
* `winner`: Boolean of whether this choice has won the contest
* ... and whatever other data is relevant for this result

The utility object has a convenient `save_results` method for updating results.

### Other data

You can also save whatever data you want in the database for reference or querying later.

The utility object has a `save` method for saving any data into any table as needed.

## Architecture

The architecture of this application is based from [ScraperWiki](https://scraperwiki.com) a platform for scraping and serving data.  The main reason for this decision is so that on or around election night, an organization can run its own server with high resources, while using the [free](https://scraperwiki.com/pricing) (for [journalists](https://wordpress.scraperwiki.com/solutions/data-journalism/)) infrastructure of ScraperWiki the rest of the year.
