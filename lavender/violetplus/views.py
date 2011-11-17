import urllib2
import json
from apiclient.discovery import build
import httplib2
from django.shortcuts import render_to_response
from datetime import datetime

USER_ID = "100389519879266040369"
API_KEY = "AIzaSyB6p8zKEB_UVBG6wxUlusIY0CFikZ26Wwk"

def fetch_g_plus():    
	http = httplib2.Http()
	service = build('plus', 'v1', developerKey=API_KEY, http=http) 

	activities = service.activities()
	request = activities.list(userId=USER_ID,
							  collection='public',
							  maxResults=10)
	activities_doc = request.execute()
	results = []
	if 'items' in activities_doc:
		for activity in activities_doc['items']:
			date_published = activity["published"]
			date = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S")
			activity["published"] = date
			results.append(activity)

	return results

def display_blog(request):
	posts = fetch_g_plus()
	context = {'request': request, 'posts': posts}
	return render_to_response('violetplus/base.html', context)