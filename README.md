# Election Night API

A set of scrapers to create an API for election night applications.  This is aimed at small to medium orgs that cannot afford services like AP or Reuters elections, or orgs that need more local results.  This is also aimed at state-level results and for states that have some sort of election night live feed.



(more details coming soon)

## Development

1. Install Python
1. Install libxml
    1. On Mac ensure XCode developer tools are installed and up to date: `xcode-select --install`
1. (optional) Use virtualenv and vitrualenvwrapper
    1. pip install virtualenv virtualenvwrapper
    1. mkvirtualenv election-night-api
1. Install libraries: pip install -r requirements.txt

## Running

* bin/ena MN -e 20141104 areas
* bin/ena MN -e 20141104 results
* bin/ena MN -e 20141104 contests

## Tests

1. py.test
