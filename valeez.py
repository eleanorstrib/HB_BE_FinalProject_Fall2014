import json
import requests
import csv
import datetime

city_destination = {
	"Boston" : "MA/Boston",
	"New York" : "NY/New_York",
	"Los Angeles" : "CA/Los_Angeles",
	"San Francisco" : "CA/San_Francisco",
	"Washington, DC" : "DC/Washington",
	"Berlin, DE" : "Germany/Berlin",
	"Cairo, EG" :"EG/Cairo",
	"London, UK" : "UK/London",
	"Mexico City, MX" : "MX/mexico_city",
	"Mumbai, IN" : "IN/Mumbai",
	"Paris, FR" : "France/Paris",
	"Rio de Janeiro, BR" : "BR/rio_de_janeiro",
	"Rome, IT" : "IT/Rome",
	"Tokyo, JP" : "JY/Tokyo"
}

#lists and dictionaries the functions below will fill in
all_calendar_days = []
clothes_to_pack = {}

all_high_temps_f = []
all_low_temps_f = []
all_pop_pct = []
all_snow_in = []

def today():
	today = datetime.date.today()
	today_date = today.day
	today_month = today.month
	return today_date, today_month

API_URL = "http://api.wunderground.com/api/ca5b10fb7297c6da/forecast10day/q/"

def inputs(today_month, today_date):
	user_destination = raw_input('where are you going?')
	user_destination = city_destination.get(user_destination)
	print user_destination
	user_depart_date = int(raw_input('what day are you leaving?'))
	# if user_depart_date > today_date + 9:
	# 	print "Date out of range, try a different date"
	# 	user_depart_date = int(raw_input('what day are you leaving?'))
	# else:
	# 	continue

	user_depart_month = int(raw_input('what month are you leaving?'))
	# if user_depart_month != today_month:
	# 	print "Date out of range, try a different month"
	# 	user_depart_month = int(raw_input('what month are you leaving?'))
	# else: 
	# 	continue


	user_number_days = int(raw_input('how long is your trip, in days?'))
	user_sex = raw_input('male or female (enter m or f)?')
	user_biz = raw_input('is this a business formal, business casual or vacation trip (enter f, c, v)?')
	return user_destination, user_depart_date, user_depart_month, user_number_days, user_sex, user_biz




API_URL = "http://api.wunderground.com/api/ca5b10fb7297c6da/forecast10day/q/"

#this function figures out which calendar days I need to query the API for
def get_the_days(user_depart_month, user_number_days, user_depart_date):
	if user_depart_month == 2:
		for i in range (0, user_number_days):
			if user_depart_date++i <= 28:
				all_calendar_days.append(user_depart_date++i)
			else:
				all_calendar_days.append((user_depart_date++i)-28)
	if user_depart_month == 4 or user_depart_month == 6 or user_depart_month == 9 or user_depart_month == 11:
		for i in range (0, user_number_days):
			if user_depart_date++i <= 30:
				all_calendar_days.append(user_depart_date++i)
			else:
				all_calendar_days.append((user_depart_date++i)-30)
	if user_depart_month == 1 or user_depart_month == 3 or user_depart_month == 5 or user_depart_month == 7 or user_depart_month == 8 or user_depart_month == 10 or user_depart_month == 12:
		for i in range (0, user_number_days):
			if user_depart_date++i <= 31:
				all_calendar_days.append(user_depart_date++i)
			else:
				all_calendar_days.append((user_depart_date++i)-31)

	
	print all_calendar_days
	return all_calendar_days

#this function calls the API and returns the forecasts for the days of the trip
def get_the_weather(all_calendar_days, user_destination):
	#these lists that will contain all of the high and low temps for the timeframe

	r = requests.get("{}{}.json".format(API_URL, user_destination))
	j = r.json()
	
	if r.status_code == 200:
		for i in range (0,9):
			for day in all_calendar_days:
				if day == j['forecast']['simpleforecast']['forecastday'][i]['date']['day']:
					all_high_temps_f.append(int(j['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit']))
					all_low_temps_f.append(int(j['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit']))
					all_pop_pct.append(int(j['forecast']['simpleforecast']['forecastday'][i]['pop']))
					all_snow_in.append(j['forecast']['simpleforecast']['forecastday'][i]['snow_allday']['in'])
				else:
					continue
	else:
		all_high_temps_f.append('error')

	#these new variables will help create the clothing list

	#testing remove when complete
	print all_high_temps_f
	print all_low_temps_f

	#keep these values
	return all_high_temps_f
	return all_low_temps_f

	# print "lows: {}".format(all_low_temps_f)
	# print "pop: {}".format(all_pop_pct)
	# print "inches of snow: {}".format(all_snow_in)

def make_the_valeez(all_high_temps_f, all_pop_pct, user_sex, user_biz, user_number_days):
	avg_high_temps_f = sum(all_high_temps_f)/len(all_calendar_days)
	avg_low_temps_f = sum(all_low_temps_f)/len(all_calendar_days)
	max_pop_pct = max(all_pop_pct)
	max_snow_in = max(all_snow_in)
	with open('garment.csv', 'rU') as f:
		reader = csv.reader(f)
		for row in reader:
			garments = row[0]
			
			if reader.line_num == 1:
				continue

			sex_column = row[1]
			if user_sex == 'f':
				sex_column = row[2]

			biz_column = row[5]
			if user_biz == 'c':
				biz_column = row[6]
			if user_biz == 'v':
				biz_column = row[7]

			temp_column = row[12]
			if avg_high_temps_f <= 55 and avg_high_temps_f > 32:
				temp_column = row[13]
			if avg_high_temps_f <= 78 and avg_high_temps_f > 55:
				temp_column = row[14]
			if avg_high_temps_f <= 90 and avg_high_temps_f > 78:
				temp_column = row[15]
			if avg_high_temps_f >= 110:
				temp_column = row[16]

			layer_column = row[4]
			tbass_column = row[3]

			if sex_column =='True' and biz_column =='True' and temp_column =='True':
				if layer_column == '0' or layer_column == '1':
					clothes_to_pack[garments] = user_number_days
				if layer_column == '2':
					clothes_to_pack[garments] = user_number_days/2
				if layer_column == '3':
					clothes_to_pack[garments] = user_number_days/2
				if layer_column == '4' or layer_column == '5':
					clothes_to_pack[garments] = 1


			rain_column = row[9]
			if max_pop_pct >= 40 and rain_column == 'True' and avg_high_temps_f >= 55:
				clothes_to_pack[garments] = 1
			

	print "Here's what you should pack: {}".format(clothes_to_pack)
	return clothes_to_pack


def main():
	# inputs()
	today_date, today_month = today()
	user_destination, user_depart_date, user_depart_month, user_number_days, user_sex, user_biz = inputs(today_date, today_month)
	
	get_the_days(user_depart_month, user_number_days, user_depart_date)
	get_the_weather(all_calendar_days, user_destination)
	make_the_valeez(all_high_temps_f, all_pop_pct, user_sex, user_biz, user_number_days)
	print "Here are all the high temperatures during your {} day trip to {} : {}.".format(user_number_days, user_destination, all_high_temps_f)
	print "Here are all the low temperatures during your {} day trip to {} : {}.".format(user_number_days, user_destination, all_low_temps_f)




if __name__=="__main__":
	main()