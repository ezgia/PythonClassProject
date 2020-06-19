
import wbdata

from flask import (
	Flask, 
	jsonify,
	request,
	render_template,
	Response,
)
from datetime import datetime #import date-time to limit wbdata table by date
app = Flask(__name__)

	
#this function retrieves financial indicator data per country from World Bank's database, by year
def get_country_gdp(country):
	indicators = {"DC.ODA.TOTL.CD": "Monetary Assistance in MM (USD)", "NY.GDP.PCAP.PP.KD": "GDP per capita (USD)"}
	country_gdp= wbdata.get_dataframe(indicators, country=country, convert_date=True, keep_levels=True)
	country_gdp['GDP per capita (USD)'] = round(country_gdp['GDP per capita (USD)'], 2)
	country_gdp['Monetary Assistance in MM (USD)'] = round(country_gdp['Monetary Assistance in MM (USD)']/10000000, 2)
	return country_gdp

#homepage, describing what to do on the page
@app.route('/')
def home():
	return render_template("home.html")

#country info page in HTML
@app.route('/<country_param>.html')
def country_info(country_param):
	try:
		country_gdp = get_country_gdp(country_param).to_html(classes="table", border=0, justify="center")
		return render_template("countrypage.html", country_param=country_param, country_gdp=country_gdp)
	except:
		return render_template("error.html")


#country info page in JSON
@app.route('/<country_param>.json')
def country_info_json(country_param):
	try:
		return Response(
			get_country_gdp(country_param).to_json(), 
			mimetype="application/json")
	except:
		return render_template("error.html")

if __name__ == '__main__':
	app.run(debug=True)