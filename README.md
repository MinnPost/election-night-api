# Election Night API

A set of scrapers to create an API for election night applications. This is aimed at small to medium orgs that cannot afford services like AP or Reuters elections, or orgs that need more local results. This works best with states that have an election night feed.

The architecture of this application is based on [ScraperWiki](https://scraperwiki.com), a platform for scraping and serving data.  The main reason for this is so that on or around election night, an organization can run its own server with high resources, while using the [free](https://scraperwiki.com/pricing) (for [journalists](https://wordpress.scraperwiki.com/solutions/data-journalism/)) infrastructure of ScraperWiki the rest of the year.

There are two parts to the API.

## The scraper tool

The `bin/ena` command is a wrapper to run each state's scraper methods. Different scraper methods can be run on differing schedules to account for how often data is updated in a given state.

* Get help on command: `bin/ena -h`
* Update results for the newest election in MN: `bin/ena MN results`
* Update areas data for specific election in MN: `bin/ana MN areas -e 20141104`

## The API

The API allows for arbitrary SQL selects of the data and returns JSON. This means it is easy to get at whatever data is needed for display on a website or other application. There are 3 possible servers you may be using.

* For development, you can use the Local API server (see below).
* For production, i.e. election night, see the Deploy instructions below.
* During off-season, you can save money by using ScraperWiki

Though the URL will change a bit, the `?q=` paramater will still be in the input mechanism for the query. Here are some examples.

* Get all contests: `/?q=SELECT * contests`
* Get a specific contest with results: `/?q=SELECT * FROM contests AS c JOIN results AS r ON c.id = r.contest_id AND c.state = r.state AND s.election = r.election WHERE c.id = 'some-contest-id'`


## Install

### Prerequisites

You may have the following already installed.

1. Install [Git](http://git-scm.com/).
1. Install [Python](https://www.python.org/downloads/).
    * Most systems already have Python installed.
1. Install [libxml](http://xmlsoft.org/).
    * On a Mac, this should be installed with XCode developer tools: `xcode-select --install`
1. (optional) Use [virtualenv](http://virtualenv.readthedocs.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
    1. `pip install virtualenv virtualenvwrapper`
        * This may need to be run with `sudo`; you should be able to tell if you get a permission error.
        * To get virtualenvwrapper to load on startup, do the following, though if you have a  non-standard Python install or are not on a bash system, see [full instructions](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). `echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bash_profile && echo "export PROJECT_HOME=$HOME/Devel" >> ~/.bash_profile && echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile && source ~/.bash_profile`

### Get code and install dependencies

1. Get the code and change to directory: `git clone https://github.com/MinnPost/election-night-api.git && cd election-night-api`
1. (optional) Make a virtualenv to work in: `mkvirtualenv election-night-api`
1. Install libraries: `pip install -r requirements.txt`

## Development

### Local API

For testing purposes, it is probably easier to use the lightweight, not production ready, local API application.

1. Scrape some data with the [scraper tool](#the-scraper-tool).
1. Run local API with: `python tests/local_api.py`
1. Make requests similar to: `http://localhost:5000/?q=SELECT * FROM contests LIMIT 10`

### Adding or managing a state

The data you need to scrape will vary from state to state, though there are some basics (see **Writing a scraper** and **Data modeling** below) and specific files and names that need to be followed. The best way to start is to copy the example and look at the comments in the file.

1. `cp states/example states/xx`
1. The `xx_meta.py` file manages each information and configuration about each election in the state.  Create the configuration as is needed for your state; there are only a couple required field.
    1. Rename `example_meta.py` to `xx_meta.py`
1. The `xx.py` holds the `Scraper` class which has the methods that are run through the command line tool.  Most of this will be specific to your state and source.
    1. Rename `example.py` to `xx.py`
    1. Make sure to call `utility.setup()` in the constructor.
1. The `test_xx.py` file is to hold tests to help unit test your files.
    1. Rename `test_example.py` to `test_xx.py`

You need to write code to translate the election results file provided by your Secretary of State or State Elections Board into a set of data fields that can be stored in the database. Since election results file formats vary widely from state to state, each state will require a custom approach, but below are some general guidelines for writing the scraper.

#### Examine data

Spend time becoming familiar with your state's election files by studying example files or files from recent elections. Are the results provided for the entire race or by precinct? Does each race have a unique identifier? Does each candidate? What results data is provided — raw vote totals, vote percentage or both?

#### Unique IDs

At a minimum, each choice in the election (e.g. candidates and ballot question responses)  and each contest must have unique identifiers. In some cases, these will already exist in a single field in the results file and can be read into your scraper (have care to verify that the IDs are in fact unique). If no single field contains a unique identifier, you will need to construct one from the data fields inside your scraper. For example, in the Minnesota scraper, we construct an ID string for each contest by combining fields for state, county, precinct district and office:

  ```
  #id-State-County-Precinct-District-Office
  base_id = 'id-' + row[0] + '-' + row[1] + '-' + row[2] + '-' + row[5] + '-' + row[3]
  ```

For more information on required fields, see **Data modeling** below.

#### Read the file
In general, you'll want to iterate through your file, manipulate the data to match the required data fields, and save those results, either by saving them to a dictionary and then writing the dictionary to the database, or by saving directly to the database.

At a minimum, you need data for a results table (data for each choice) and a contests table (data for each race/office).

The minimum required results fields are `id, state, election, updated, contest_id, choice, party, votes, percentage, winner`. The minimum required contests fields are `id, state, election, updated, title, precincts_reporting, total_precincts, percent_reporting, total_votes, seats`. (Note: state, election and updated can be filled using `self.util` methods. See **Data modeling** below.)

In both cases, additional fields can be added to the tables as needed for your specific elections. The `id` in the contests table should match the `contest_id` in the results table and is used to link candidates/options to their overall races. For more information on required fields, see *Data modeling* below.

Some of these data fields may be accessible directly from the results file, but others will require calculation or other manipulation inside the scraper script. Look at existing state scrapers for some examples of this data processing.

#### Manual data

In some cases, you may want to add in additional election data not available in the election results file. An easy way to do this is to create a Google Spreadsheet with the additional data. The `utility.google_spreadsheet(spreadsheet_id, worksheet_id, gs_types_dict)` method gives you all the rows in a specific Google Spreadsheet which you can iterate over to read additional data for writing to the `results` or `contests` tables. You probably want to match the unique IDs for either results or contests in this spreadsheet.

For more information, see **Utility library** below.

### Utility library

In the `Scraper` object, a `utility` object will be passed in. This will be a `ENAUtility` class instance with connections made to the election that is being processed.

* `utility.state`: The state that is being processed.
* `utility.election_id`: The election ID that is being processed.
* `utility.election`: The election meta data found in `xx_meta.py` for the election being processed.
* `utility.setup()`: This connects to the correct database.
* `utility.timestamp()`: Get an integer timestamp of right now.
* `utility.save(id_array, data_dict, table_name, index_method)`: Save (insert or update) a row or rows to the database. The index method will be called on the first insert to the table.
* `utility.has_table(table_name)`: Check if table exists in the database.
* `utility.save_meta(key_name, value)`: Save a value to the meta table.
* `utility.google_spreadsheet(spreadsheet_id, worksheet_id, gs_types_dict)`: Get data from a Google Spreadsheet, specific sheet. If dictionary type is given, the utility will attempt to type the data.
* `utility.save_results(data)`: Save results data. Checks if the basic results fields are there.
* `utility.save_contests(data)`: Save contests data. Checks if the basic contests fields are there.
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

Contests are the generic word for races, ballot questions, referendums, etc. This data should have at least the following fields, but you can have as many more fields as you want.

* `id`: A unique ID for the contest across the state and election
* `state`: State code, can be provided with `self.util.state`
* `election`: Election ID, can be provided with `self.util.election_id`
* `updated`: Timestamp integer of last updated, can use `self.util.timestamp()`
* `title`: Title of contest, e.g. “U.S. Rep. District 2” or “Proposed constitutional amendment”
* `precincts_reporting`: Integer number of precincts reporting
* `total_precincts`: Integer number of total precincts effected by contest
* `percent_reporting`: Float percentage (85.0, not 0.85) of precincts reporting
* `total_votes`: Integer of total votes cast
* `seats`: Number of seats that can be won, usually 1
* ... and whatever other data is relevant for this contest

The utility object has a convenient `save_contests` method for updating results.

### Results

Results are data for each candidate, write-in, answer, etc. for each contest. There will generally be at least two rows of results per contest.

* `id`: A unique ID for the candidate/answer/choice/etc. across the state and election.
* `state`: State code, can be provided with `self.util.state`
* `election`: Election ID, can be provided with `self.util.election_id`
* `updated`: Timestamp integer of last updated, can use `self.util.timestamp()`
* `contest_id`: The corresponding contest ID from the contests table
* `choice`: The name of the candidate or question answer (Yes or No usually)
* `party`: Party identifier, such as `D` or `R`
* `votes`: Integer number of votes this choice received so far
* `percentage`: Float percentage (85.0, not 0.85) of the number of total votes in contest so far
* `winner`: Boolean of whether this choice has won the contest
* ... and whatever other data is relevant for this result

The utility object has a convenient `save_results` method for updating results.

### Other data

You can also save whatever data you want in the database for reference or querying later.

The utility object has a `save` method for saving any data into any table as needed.

## Deploy

For election night, the idea is to install this on a resourceful server; overall the server should have most resources towards I/O as opposed to memory or CPU, though those things are needed as well. The following instructions and the provided configuration are aimed at installing the API on an Ubuntu server (on EC2).

It is suggested to use `Ubuntu Server 14.04 LTS 64-bit (ami-9eaa1cf6)` AMI from EC2.  Your Security Group will need port `80` (HTTP) open and whatever port you will SSH into (default `22`).

Note that these instructions are for a fresh server without other apps running on it. Please look at the instructions and configurations in detail if you have existing apps running on the server.

### Code, libraries, and prerequisites

1. Make sure Ubuntu is up to date: `sudo aptitude update && sudo aptitude safe-upgrade`
1. Install system and python base packages: `sudo aptitude install git-core git python-pip python-dev build-essential python-lxml sqlite3 nginx-full fcgiwrap`
1. Install python base packages: `sudo pip install --upgrade pip && sudo pip install --upgrade virtualenv`
1. Go to the home directory; you can put the code somewhere else but you may have to manually update other parts of the deploy: `cd ~`
1. Get the code: `git clone https://github.com/MinnPost/election-night-api.git && cd election-night-api`
1. `sudo pip install -r requirements.txt`
1. Add path so we have reference for later: `echo "export ENA_PATH=$(pwd)" >> ~/.bash_profile`

### Webserver

As this is meant to emulate how ScraperWiki works, it uses Dumptruck, FastCGI and Nginx to create an API for the scraped data in the sqlite database.

1. [Dumptruck](https://github.com/scraperwiki/dumptruck-web) is a Python script to create an API on-top of an sqlite database.  It's built by ScraperWiki and also handles multiple user location.
    1. `sudo git clone https://github.com/scraperwiki/dumptruck-web.git /var/www/dumptruck-web && sudo chown -R www-data:www-data /var/www/dumptruck-web && sudo pip install -r /var/www/dumptruck-web/requirements.txt`
1. FCGIWrap is used to create an interface between the Dumptruck and Nginx. We use a simple script to configure the number of children to use.
    1. `sudo cp deploy/fcgiwrap /etc/default/fcgiwrap`
    1. Restart service (note that this can take a minute): `sudo service fcgiwrap restart`
1. Nginx is used as the top level web server.  It allows for caching and other niceties.  This copies our config, enables it and removes the default.
    1. `sudo cp deploy/nginx-scraper-api.conf /etc/nginx/sites-available/election-night-api.conf && sudo ln -s /etc/nginx/sites-available/election-night-api.conf /etc/nginx/sites-enabled/election-night-api.conf && sudo rm /etc/nginx/sites-enabled/default`
    1. Restart service: `sudo service nginx restart`
    1. Test with something like: http://ec2-XX-XX-XX.compute-1.amazonaws.com/sql?box=ubuntu/election-night-api&method=sql&q=SELECT%20*%20FROM%20results%20LIMIT%2010
        * The `box` paramater is essentially the directory path where the `scraperwiki.sqlite` file resides.  TODO: Figure out how to make nginx provide a default for this.
        * Update the `box` parameter if code was installed in another place.

### Cron

For election night, and leading up to it, you will want the scraper tool to run on an interval, probably with some methods running occasionally, while at least one running continuously.  Utilizing cron for this is best. There is a helpful wrapper, `deploy/continuous-wrapper.sh` that will run the scraper tool continuously.

* Set the `ENA_PATH` in the cron file as this is not carried over from the user: `ENA_PATH=/home/ubuntu/election-night-api`
* Get results continuously: `* * * * * $ENA_PATH/deploy/continuous-wrapper.sh MN results`
* Log to home directory: `* * * * * $ENA_PATH/deploy/continuous-wrapper.sh MN results > ~/logs/ena.log`
* Run less important scrapes: `0 7 * * * $ENA_PATH/bin/ena MN questions`

## Migration to ScraperWiki

For non-election time, it makes sense to save resources and use the ScraperWiki architecture.  Run the following to get the scraper up on the ScraperWiki architecture.

1. Make sure you have an account on ScraperWiki
1. Create new, or use the existing, scraper for the election results.
1. Run ...
