import requests
import os
# import twilio
from twilio.rest import Client

# use constant variables for your personal and twilio numbers

MYTWILIOPHONENUMBER = "[Your Twilio number]"
MYPHONENUMBER = "[Your personal phone number]"

# Initialize twilio sid and token values

account_sid = '[Your twilio sid]'
auth_token = '[Your twilio token]'

# Initialize open weather map url and params

API_key = "[Your 'Open Weather Map' api key]"
lat = "[lat of the city you want the weather data]"
lon = "[lon of the city you want the weather data]"
api_url = "https://api.openweathermap.org/data/2.5/forecast"

weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": API_key,
    "cnt": 4,
    "units": "metric",
    "lang":"el",
}

# Request
response = requests.get(api_url, params=weather_params)
response.raise_for_status()

# Initialize 3 lists. 1 for the temps, 1 for the weather group, and 1 to combine them

listOfTemps = []
listOfWeatherGroup = []
weatherList = []

# Getting data per three hour.
# The data we will use is the temperature 'feels like' to humans
# And the weather group (clouds, snow, rain etc)

for per_three_hour_data in response.json()['list']:
    temp = per_three_hour_data['main']['feels_like']
    listOfTemps.append('%.1f' % temp)
    weather_id = per_three_hour_data['weather'][0]['id']
    weather_group = per_three_hour_data['weather'][0]['description']
    listOfWeatherGroup.append(weather_group)

time = 0
for i in range(len(listOfTemps)):
    time += 1
    temp_value = f"The temperature for the next {hours*3} hours will be: {listOfTemps[i]} C", listOfWeatherGroup[i]    
    weatherList.append(temp_value)

weatherList = ('\n\n'.join(map(str, weatherList))).replace("(","").replace(")","")

print(weatherList)

# Using the twilio module to send the message

client = Client(account_sid, auth_token)
message = client.messages \
           .create(
                body=weatherList,
                from_=MYTWILIOPHONENUMBER,
                to=MYPHONENUMBER
               )
print(message.sid)
