#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import sys
import requests
from filecache import filecache


# config, change these to what you'd like
city_name = "Burnaby"
country_name = "Canada"
api_key = "CHANGEME"


# cache for 30 minutes to reduce API calls
@filecache(60*30)
def get_api_response(url):
    print "Getting response from %s" % url
    response = requests.get(url)
    return response

if __name__ == "__main__":

    api_url = "http://api.wunderground.com/api/%s/%s/q/%s/%s.json"

    forecast_response = \
        get_api_response(api_url %
                         (api_key,
                          "forecast",
                          country_name, city_name))

    forecast_response.raise_for_status()

    fjson = forecast_response.json()

    if "error" in fjson["response"]:
        print "Unable to get forecast data from\
 weatherunderground: %s" % fjson["response"]["error"]["description"]
        print "Did you remember to specify your API key? (Currently %s)" \
            % api_key
        sys.exit(1)

    # first item in the forecast is today's
    today_forecast = fjson["forecast"]["simpleforecast"]["forecastday"].pop(0)
    today_high = int(today_forecast["high"]["celsius"])

    print u"Today is forecasted with a high of %s˚C." % today_high

    for item in fjson["forecast"]["simpleforecast"]["forecastday"]:
        forecasted_high = int(item["high"]["celsius"])
        weekday = item["date"]["weekday"]

        difference = "about the same as"
        if (forecasted_high > (today_high + 1)):
            difference = "warmer than"
        elif (forecasted_high < (today_high - 1)):
            difference = "cooler than"

        print u"%s (at %s˚C) is predicted to be %s today." % \
            (weekday, forecasted_high, difference)
