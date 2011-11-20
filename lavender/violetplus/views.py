from apiclient.discovery import build
import httplib2
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
from forms import NextPageForm
import re

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
	if 'items' in activities_document:
		for activity in activities_doc['items']:
			modify_activity(activity)
	return activities_document


def display_blog(request):
	token = None
	if request.method == 'POST':
		submitted_form = NextPageForm(request.POST)
		if submitted_form.is_valid():
			token = submitted_form.cleaned_data['token']
	posts = fetch_g_plus_activities(10, token)
	context = {'request': request, 'posts': posts}
	if 'nextPageToken' in posts:
		page_token = posts['nextPageToken']
		form = NextPageForm(initial={'token':page_token})
		context['form'] = form
	return render_to_response('violetplus/base.html', context, 
		context_instance=RequestContext(request))

def display_post(request, act_id):
	post = fetch_g_plus_activity(act_id)
	context = {'request': request, 'post': post}
	return render_to_response('violetplus/post.html', context)