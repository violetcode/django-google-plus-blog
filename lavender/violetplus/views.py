import urllib2
import json
import google-api-python-client

API_KEY = "AIzaSyB6p8zKEB_UVBG6wsU1usIY0CFikZ26Wwk"
USER_ID = "100389519879266040369"

def fetch_g_plus():     
	url = "https://www.googleapis.com/plus/v1/people/{0}/activities/public?key={1}".format(USER_ID, API_KEY)
