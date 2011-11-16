import urllib2
import json
import apiclient
import httplib2
from django.shortcuts import render_to_response

API_KEY = "AIzaSyB6p8zKEB_UVBG6wsU1usIY0CFikZ26Wwk"
USER_ID = "100389519879266040369"

def fetch_g_plus():    
	http = httplib2.Http()
	service = apiclient.discovery.build('plus', 'v1', developerKey=API_KEY, http=http) 

	activities = service.activities()
	request = activities.list(userId=USER_ID,
							  collection='public',
							  maxResults=10)
	activities_doc = request.execute()
	results = []
	if 'items' in activities_doc:
		for activity in activities_document['items']:
			results.append(activity)

	return results

def display_blog(request):
	posts = fetch_g_plus()
	context = {'request': request, 'posts': posts}
	return render_to_response('violetplus/view_blog.html', context)