from apiclient.discovery import build
import httplib2
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
import re

from django import template

register = template.Library()

USER_ID = "100389519879266040369"
API_KEY = "AIzaSyB6p8zKEB_UVBG6wxUlusIY0CFikZ26Wwk"

http = httplib2.Http()
service = build('plus', 'v1', developerKey=API_KEY, http=http) 

def modify_activity(activity):
	date_published = activity["published"].strip(".000Z")
	activity["published"] = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S")
	content = activity["object"]["content"]
	title_re = re.compile(r'^<b>(?P<title>.*)</b><br /><br />')
	matches = title_re.search(content)
	if matches:
		title = matches.group('title')
		activity['title'] = title
		activity["object"]["content"] = title_re.sub("", content)


def fetch_g_plus_activities(limit, nextPageToken=None):  
	activities = service.activities()
	if not nextPageToken:
		request = activities.list(userId=USER_ID,
							  collection='public',
							  maxResults=limit)
	else:
		request = activities.list(userId=USER_ID,
								  collection='public',
								  maxResults=limit,
								  pageToken=nextPageToken)
	activities_doc = request.execute()
	if 'items' in activities_doc:
		for activity in activities_doc['items']:
			modify_activity(activity)
	return activities_doc

def fetch_g_plus_activity(activ_id):
	activities_resource = service.activities()
	activities_document = activities_resource.get(activityId=activ_id).execute()
	modify_activity(activities_document)
	return activities_document


@register.inclusion_tag('violetplus/latest_entries.html')
def render_latest_blog_entries(num):
	token = None
	posts = fetch_g_plus_activities(num, token)
	return {'posts': posts}