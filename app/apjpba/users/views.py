# coding=utf8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_backends
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from apjpba.items.models import Item
from django.core.validators import email_re #register
from django.contrib.auth.models import User #register, username_exists, email_exists
from django.core.mail import send_mail
from session import Session
import string, random
import users.facebook as facebook
import urllib
import urllib2
import random
import poplib
import string
import time
import re
import json


def moodle_check_login(username, password):
	
	#urls
	login_url = "http://moodle.sc-celje.si/ker/login/index.php"
	
	login_data = {
	'username': username,
	'password': password,
	'testcookies': '1'
	}
	
	try:
		data = urllib.urlencode(login_data)
		
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
		urllib2.install_opener(opener)
		
		f = opener.open(login_url)
		y = f.read()
		f.close()
		
		f = opener.open(login_url, data)
		y = f.read()
		f.close()
		
		m = re.search('<div class="logininfo">(.*)</div>', y)
		m2 = m.group(1).replace("  ", " ")
		m3 = re.search('<a href=(.*)>(.*)</a>', m2)
		
		a=re.match('<a href="(.*)">(.*)</a> \(', m3.group(0))
		
		
		name = a.group(2)
		
		profile_url = a.group(1).replace("view.php", "edit.php")
		
		f = opener.open(profile_url)
		y = f.read()
		f.close()
		
		em = re.search('<input maxlength="100" size="30" name="email" type="text" value="(.*)"', y)
		em2 = em.group()
		em3 = re.match('<input maxlength="100" size="30" name="email" type="text" value="(.*)" onblur', em2)
		email = em3.group(1)
		
		return {'name': name, 'email': email}
	except:
		return None

def random_string(x):
	chars = string.letters + string.digits
	
	newpasswd = ''
	
	for i in range(x):
		newpasswd = newpasswd + chars[random.randint(0,len(chars)-1)]
	
	return newpasswd

def is_valid_email(email):
    return True if email_re.match(email) else False
   
def username_exists(username):
	try:
		User.objects.get(username=username)
	except User.DoesNotExist:
		return False
	return True

def email_exists(email):
	try:
		User.objects.get(email=email)
	except User.DoesNotExist:
		return False
	return True

def change_password(user, password = None):
	if password == None:
		password = random_string(6)
	
	user.set_password(password)
	user.save()
	
	return password

def login_or_register(request, email, username):
	if email_exists(email):
			#user exists
			#log him in
		pass
	else:
		#create new user
		u = User(username=username, password='mypass', email=email)
		u.save()
		
	uid = User.objects.get(email=email)
	user = uid
	
  	# In lieu of a call to authenticate()
  	
  	#ss
	#login(self.request, user)
  	
  	
  	backend = get_backends()[0]
	user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
  	auth_login(request, user)
  	#return HttpResponse(x['name'])

def fblogin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	
	user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
	
	if user:
		graph = facebook.GraphAPI(user["access_token"])
		profile = graph.get_object("me")
		
		if 'first_name' in profile and 'last_name' in profile and 'email' in profile:
			login_or_register(request, profile['email'], profile['first_name']+ ' ' + profile['last_name'])
			
			request.session['facebook'] = True
			
			if 'next' in request.GET:
				url = request.GET['next']
			
			
			if 'url' in request.POST and request.POST['url'] != '':
				return HttpResponseRedirect('/' + request.POST['url'][1:])
			else:
				return HttpResponseRedirect('/')
		else:
			return HttpResponse('Napaka pri prijavi!')
	else:
		return HttpResponseRedirect('/')

def fbmoodle_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
		
	error = ''
	
	if 'username' in request.POST and 'password' in request.POST:
		x=moodle_check_login(request.POST['username'], request.POST['password'])
		
		if not x:
			error = 'Uporabniško ime in/ali geslo je napačno.'
		else:
			login_or_register(request, x['email'], x['name'])
			
			if 'next' in request.GET:
				url = request.GET['next']
			
			
			if 'url' in request.POST and request.POST['url'] != '':
				return HttpResponseRedirect('/' + request.POST['url'][1:])
			else:
				return HttpResponseRedirect('/')
		
	return render_to_response('users/fbmoodle_login.html',
							{'error': error},
							context_instance = RequestContext(request))

def fbchannel(request):	
	return HttpResponse('<script src="http://connect.facebook.net/en_US/all.js"></script>');

"""
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	
	error = ''
	url = ''
	
	if 'session' in request.COOKIES:
		sessname = request.COOKIES['session']
		
		try:
			s = Session(sessname)
		except:
			return HttpResponseRedirect('http://www.apj-pba.com/')
		
		if s.get('email') and s.get('name'):
			if email_exists(s.get('email')):
					#user exists
					#log him in
				pass
			else:
				#create new user
				u = User(username=s.get('name'), password='mypass', email=s.get('email'))
				u.save()
				
			uid = User.objects.get(email=s.get('email'))
			user = uid
			
        	# In lieu of a call to authenticate()
        	
        	#ss
    		#login(self.request, user)
		  	
		  	
		  	backend = get_backends()[0]
	  		user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
		  	auth_login(request, user)
		  	#return HttpResponse(x['name'])
		  	
		  	if 'next' in request.GET:
				  url = request.GET['next']
			
			
			if 'url' in request.POST and request.POST['url'] != '':
				return HttpResponseRedirect('/' + request.POST['url'][1:])
			else:
				return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')


def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	
	errors = []
	username = ''
	email = ''
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']
		email = request.POST['email']
		
		secret_word = request.POST['sw']
		
		if not secret_word.lower() == 'e4e':
			errors.append('Napačna beseda!')
		
		if not password == password2:
			errors.append('Gesli se ne ujemata!')
		
		if not is_valid_email(email):
			errors.append('Email naslov ni pravilen!')
		
		if username_exists(username):
			errors.append('Uporabnik z enakim uporabnikom že obstaja!')
		
		if email_exists(email):
			errors.append('Uporabnik z enakim email naslovom že obstaja!')
		
		if len(errors) == 0:
			#register the user
			user = User.objects.create_user(username, email, password)
			user.save()
			
			user2 = authenticate(username=username, password=password)
			auth_login(request, user2)
			
			return HttpResponseRedirect('/')
	
	return render_to_response('users/register.html', {'errors': errors, 'username': username, 'email': email},
		context_instance=RequestContext(request))
"""

def logout(request):
	try:
		del request.session['facebook']
	except KeyError:
		pass

	auth_logout(request)
	return HttpResponseRedirect('/')
	
@login_required
def show(request, id):
	user = get_object_or_404(User, id=id)
	public_items = Item.objects.filter(user=user,is_private=False).order_by('-pub_date')
	users = User.objects.all().order_by('username')
	
	return render_to_response('users/show.html', {'user_info': user, 'public_items': public_items, 'users': users}, context_instance=RequestContext(request))

"""
def reset_password(request):
	error = ''
	
	if 'username' in request.POST or 'email' in request.POST:
		if 'username' in request.POST and len(request.POST['username']) > 0:
			#Check user by username
			try:
				u = User.objects.get(username=request.POST['username'])
				
				password = change_password(u)
				
				send_mail('Novo geslo za Apj Pba', 'Pozdravljen ' + u.username + ',\n\ntvoje novo geslo za spletno stran Apj Pba je: ' + password + '\n\nApj Pba\nwww.apj-pba.com', 'info@apj-pba.com',
    [u.email], fail_silently=False)
			except:
				return render_to_response('users/reset-password.html', {'error': 'Uporabnik s tem uporabniškim imenom ne obstaja!'}, context_instance=RequestContext(request))

		else:
			#Check user by email
			try:
				u = User.objects.get(email=request.POST['email'])
				
				password = change_password(u)
				
				send_mail('Novo geslo za Apj Pba', 'Pozdravljen ' + u.username + ',\n\ntvoje novo geslo za spletno stran Apj Pba je: ' + password + '\n\nApj Pba\nwww.apj-pba.com', 'info@apj-pba.com', [u.email], fail_silently=False)
			except:
				return render_to_response('users/reset-password.html', {'error': 'Uporabnik s tem email naslovom ne obstaja!'}, context_instance=RequestContext(request))
		
		return render_to_response('users/reset-password-done.html', {}, context_instance=RequestContext(request))
	else:
		return render_to_response('users/reset-password.html', {}, context_instance=RequestContext(request))
"""
#@login_required
#def my_files(request):
#	items = request.user.item_set.all()
#	
#	return render_to_response('users/my_files.html', {'items': items},
#		context_instance=RequestContext(request))