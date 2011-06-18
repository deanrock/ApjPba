# coding=utf8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import string, random, os, sys, datetime, time
from django.conf import settings
from django.http import Http404
from apjpba.discussions.models import Topic, Post, LastView

def add_new_post(user_id, post_content, topic):
	p = Post(user=user_id, post=post_content)
	p.save()
	
	topic.posts.add(p)
	topic.modified_date = p.pub_date
	topic.modified_user = p.user
	topic.save()
	
	return p

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Show all topics, descending by last post's pub_date
@login_required
def index(request):
	topics = Topic.objects.all().order_by('-modified_date')
	
	return render_to_response('discussions/show-topics.html', {'topics': topics}, context_instance=RequestContext(request))

@login_required
def show(request, topic_id):
	topic = get_object_or_404(Topic, id=topic_id)
	
	posts = topic.posts.all().order_by('pub_date')
	
	last_visit = topic.get_last_visit(request.user)
	
	if last_visit == None:
		last_visit = datetime.datetime.min
	
	topic.mark_as_read(request.user)
	
	return render_to_response('discussions/topic.html', {'topic': topic, 'posts': posts, 'last_visit': last_visit}, context_instance=RequestContext(request))

@login_required
def new_topic(request):
	if request.POST:
		try:
			t = Topic(name=request.POST['name'], user=request.user)
			t.save()
			
			add_new_post(request.user, request.POST['bbcode'], t)
			
			return HttpResponseRedirect('/discussions/topic/' + str(t.id))
		except:
			None
	
	return render_to_response('discussions/new-topic.html', {}, context_instance=RequestContext(request))

@login_required
def new_post(request):
	if not 'topic' in request.POST and not is_number(request.POST['topic']):
		raise Http404
	
	topic = get_object_or_404(Topic, id=request.POST['topic'])
	
	if not 'bbcode' in request.POST:
		raise Http404
	
	p = add_new_post(request.user, request.POST['bbcode'], topic)
	
	return HttpResponseRedirect('/discussions/topic/' + str(topic.id) + '#post' + str(p.id))