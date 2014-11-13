# Election Night API

A set of scrapers to create an API for election night applications.  This is aimed at small to medium orgs that cannot afford services like AP or Reuters elections, or orgs that need more local results.  This is also aimed at state-level results and for states that have some sort of election night live feed.

## Running scraper

The `bin/ena` command is a wrapper to run each state scraper methods.  It is arbitrary what method to run, as the need to run certain methods on certain schedules can change from state to state.

* Get help on command: `bin/ena -h`
* Update results for the newest election in MN: `bin/ena MN results`
* Update areas data for specific election in MN: `bin/ana MN areas -e 20141104`

## Development

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

### Adding or managing a state

Scraping is arbitrary, though there are some basics (see Data modeling below) and specific files and names that need to be followed.  The best way to start is copy the example and then look at the comments in the file.

1. `cp states/example states/xx`
1. The `xx_meta.py` file manages each information and configuration about each election in the state.  Create the configuration as is needed for your state; there are only a couple required field.
    1. Rename `example_meta.py` to `xx_meta.py`
1. The `xx.py` holds the `Scraper` class which has the methods that are run through the command line tool.  Most of this will be specific to your state and source.
    1. Rename `example.py` to `xx.py`
    1. Make sure to call `utility.setup()` in the constructor.
1. The `test_xx.py` file is to hold tests to help unit test your files.
    1. Rename `test_example.py` to `test_xx.py`

### Utility library

In the `Scraper` object, a `utility` object will be passed in.  This will be a `ENAUtility` class instance with connections made to the election that is being processed.

* `utility.state`: The state that is being processed.
* `utility.election_id`: The election ID that is being processed.
* `utility.election`: The election meta data found in `xx_meta.py` for the election being processed.
* `utility.setup()`: This connects to the correct database.
* `utility.timestamp()`: Get an integer timestamp of right now.
* `utility.save(id_array, data_dict, table_name, index_method)`: Save (insert or update) a row or rows to the database.  The index method will be called on the first insert to the table.
* `utility.has_table(table_name)`: Check if table exists in the database.
* `utility.save_meta(key_name, value)`: Save a value to the meta table.
* `utility.google_spreadsheet(spreadsheet_id, worksheet_id, gs_types_dict)`: Get data from a Google Spreadsheet, specific sheet.  If dictionary type is given, the data will attempt to be typed.
* `utility.save_results(data)`: Save results data.  Checks if the basic results fields are there.
* `utility.save_contests(data)`: Save contests data.  Checks if the basic contests fields are there.
* 'utility.scrape()': Just a link to [scraperwiki.scrape](https://github.com/scraperwiki/scraperwiki-python#scraping).
* `utility.sql`: A link to [scraperwiki.sql]](https://github.com/scraperwiki/scraperwiki-python#saving-data).

### Tests

`py.test` will find all python files with [specific names](http://pytest.org/latest/goodpractises.html#test-discovery) in a given directory.

1. Run all the tests (including all the states): `py.test`
1. Run all the state tests: `py.test states/`
1. Run a specific state test: `py.test states/mn/`

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
