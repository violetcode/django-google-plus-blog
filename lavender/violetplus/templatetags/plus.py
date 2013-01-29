from apiclient.discovery import build
import httplib2
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
import os, re

from django import template

register = template.Library()

USER_ID = os.environ['USER_ID']
API_KEY = os.environ['API_KEY']

http = httplib2.Http()
service = build('plus', 'v1', developerKey=API_KEY, http=http) 

def modify_activity(activity):
	published = activity["published"]
	date_published = re.sub("\.\d*Z$", '', activity["published"])
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


@register.inclusion_tag('violetplus/latest_entries.htm')
def render_latest_blog_entries(num):
	posts = fetch_g_plus_activities(num)
	return {'posts': posts}