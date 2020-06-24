# World Bank Financial Indicators

World Bank Financial Indicators is a Flask web application that retrieves financial health indicator, GDP per capita (USD), for countries based on World Bank database, utilizing the wbdata library of Python.

## Installation

The following Python packages must be installed to use this project:
1. wbdata: use "pip install wbdata"
3. flask: use "pip install Flask"

## Usage

Run main.py in your terminal.

Enter resulting local host address generated by Flask into your web browser. 

Follow directions on the homepage; enter country codes to either the Search bar on the navigation pane, or the host route (e.g. for United States of America: /USA.html, /USA.json, or /USA.csv) to access information about a country. If you enter the wrong country code, an error page will appear instead.

## APIs used:

The following two public APIs are used to create this website's content:
1. World Bank, via wbdata python interface: https://wbdata.readthedocs.io/en/stable/
2. Country Flags: https://www.countryflags.io/
