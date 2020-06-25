
import wbdata

import flagcodes #imports dicts for country codes for showing the corresponding country flag

from flask import (
	Flask, 
	jsonify,
	request,
	render_template,
	Response,
)

import datetime #import date-time functions to fulfill wbdata parameters

import requests

import json

API_BASE = "https://www.mapbox.com/pk.eyJ1IjoiZXpnaWEiLCJhIjoiY2tidTVjN3YxMDB0MTJ5bGQyY3Q5OGJjaSJ9.kKH2fgIziAx7_mkZjTcnrg"
resource = 'styles/v1/ezgia/satellite-v9.html'
r = requests.get(f"{API_BASE}/{resource}")
app = Flask(__name__)

	
#this function retrieves financial indicator data per country from World Bank's database, by year
def get_country_gdp(country):
	country_gdp = wbdata.api.get_data("NY.GDP.PCAP.CD", country=country, data_date=(datetime.date(2009,1,1), datetime.date(2018,1,1)), convert_date=False, pandas=False, column_name='GDP per Capita', keep_levels=False)
	country_gdp = wbdata.api.convert_to_dataframe(country_gdp, "GDP per capita (USD)")
	country_gdp['GDP per capita (USD)'] = round(country_gdp['GDP per capita (USD)'], 0)
	country_gdp = country_gdp.drop(columns="country")
	country_gdp.set_index(country_gdp['date'], drop=True, append=False, inplace=True, verify_integrity=False)
	country_gdp = country_gdp.drop(columns="date")
	return country_gdp

#this function retrieves YoY change for financial indicators for a country
def get_yoy_change(country):
	country_gdp = get_country_gdp(country)
	try:
		yoy_change = round((country_gdp['GDP per capita (USD)'][0]/country_gdp['GDP per capita (USD)'][1]-1)*100, 0)
	except:
		yoy_change = 0
	return yoy_change

#homepage, describing what to do on the page
@app.route('/')
def home():
	return render_template("home.html")

#country info page in HTML
@app.route('/<country_param>.html')
def country_info(country_param):
	try:
		country_gdp = get_country_gdp(country_param).to_html(classes="table", border=0, justify="center")
		yoy_change = get_yoy_change(country_param)
		yoy_change_str = str(yoy_change)+"%"
		flagcode = flagcodes.ISO2dict[country_param]
		country_name = flagcodes.ISOcountryname[country_param]
		return render_template("countrypage.html", yoy_change=yoy_change, yoy_change_str=yoy_change_str, country_param=country_param, country_gdp=country_gdp, flagcode=flagcode, country_name = country_name)
	except:
		if country_param in flagcodes.ISO2dict.keys():
			flagcode = flagcodes.ISO2dict[country_param]
			return render_template("errorwflag.html", country_param = country_param, flagcode=flagcode) #error page that is served when API connection is unavailable
		else:
			return render_template("error.html") #error page that is served when user enters an invalid country code

#country info page in JSON
@app.route('/<country_param>.json')
def country_info_json(country_param):
	try:
		return Response(
		get_country_gdp(country_param).to_json(), 
		mimetype="application/json")
	except:
		if country_param in flagcodes.ISO2dict.keys():
			flagcode = flagcodes.ISO2dict[country_param]
			return render_template("errorwflag.html", country_param = country_param, flagcode=flagcode)
		else:
			return render_template("error.html")

#country info page in CSV
@app.route('/<country_param>.csv')
def country_info_csv(country_param):
	try:
		return Response(
		get_country_gdp(country_param), 
		mimetype="application/csv")
	except:
		if country_param in flagcodes.ISO2dict.keys():
			flagcode = flagcodes.ISO2dict[country_param]
			return render_template("errorwflag.html", country_param = country_param, flagcode=flagcode)
		else:
			return render_template("error.html")

#country info page utilizing POST method from search bar on the navigation panel
@app.route('/', methods=['POST'])
def my_form_post():
	try:
		country_param = request.form['country']
		country_gdp = get_country_gdp(country_param).to_html(classes="table", border=0, justify="center")
		yoy_change = get_yoy_change(country_param)
		yoy_change_str = str(yoy_change)+"%"
		flagcode = flagcodes.ISO2dict[country_param]
		country_name = flagcodes.ISOcountryname[country_param]
		return render_template("countrypage.html", yoy_change=yoy_change, yoy_change_str=yoy_change_str, country_param=country_param, country_gdp=country_gdp, flagcode=flagcode, country_name = country_name)
	except:
		if country_param in flagcodes.ISO2dict.keys():
			flagcode = flagcodes.ISO2dict[country_param]
			return render_template("errorwflag.html", country_param = country_param, flagcode=flagcode)
		else:
			return render_template("error.html")

if __name__ == '__main__':
	app.run(debug=True)