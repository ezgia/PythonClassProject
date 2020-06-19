import wbdata

from datetime import datetime


	

#def get_country_gdp(country):
	#indicators = {"IC.BUS.EASE.XQ": "doing_business", "NY.GDP.PCAP.PP.KD": "gdppc"}
	#country_gdp= wbdata.get_dataframe(indicators, country=country, convert_date=True)

if __name__ == '__main__':
	indicators = wbdata.get_indicator(source=32)
	print(*indicators, sep = "\n")
