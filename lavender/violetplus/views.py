import urllib2
import json
from apiclient.discovery import build
import httplib2
from django.shortcuts import render_to_response
from datetime import datetime

USER_ID = "100389519879266040369"
API_KEY = "AIzaSyB6p8zKEB_UVBG6wxUlusIY0CFikZ26Wwk"

http = httplib2.Http()
service = build('plus', 'v1', developerKey=API_KEY, http=http) 

def convert_published_to_datetime(activity):
	date_published = activity["published"].strip(".000Z")
	activity["published"] = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S")

def fetch_g_plus_activities(limit):    
	activities = service.activities()
	request = activities.list(userId=USER_ID,
							  collection='public',
							  maxResults=limit)
	activities_doc = request.execute()
	if 'items' in activities_doc:
		for activity in activities_doc['items']:
			convert_published_to_datetime(activity)
	return activities_doc

def fetch_g_plus_actvitity(activ_id):
	activities_resource = service.activities()
	activities_document = activities_resource.get(activityId=activ_id).execute()
	if 'items' in activities_document:
		convert_published_to_datetime(activities_document['items'])
	return activities_document


def display_blog(request):
	posts = fetch_g_plus_activities(10)
	context = {'request': request, 'posts': posts}
	return render_to_response('violetplus/base.html', context)