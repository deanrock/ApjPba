# coding=utf8
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from apjpba.items.models import Item, Subject, Comment, RatingUsers
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
import string, random, os, sys
from django.utils import simplejson
import datetime, time
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import Http404

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Upload
class CustomException(Exception):
   def __init__(self, value):
       self.parameter = value
   def __str__(self):
       return repr(self.parameter)

def handle_uploaded_file(f, id):
	destination = open(settings.FILES_URL + '/' + id, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	
	destination.close()

def random_string(x):
	chars = string.letters + string.digits
	
	newpasswd = ''
	
	for i in range(x):
		newpasswd = newpasswd + chars[random.randint(0,len(chars)-1)]
	
	return newpasswd

#View methods
@login_required
def index(request, type = ''):
	selected_subject = None
	
	if 'subject' in request.GET and is_number(request.GET['subject']):
		s = Subject.objects.get(id=request.GET['subject'])
		if s:
			selected_subject = s.id
			
	#files
	if type == 'my-files':
		if selected_subject == None:
			items = Item.objects.filter(is_private=True,user=request.user).order_by('-pub_date')
		else:
			items = Item.objects.filter(is_private=True,user=request.user,subject=selected_subject).order_by('-pub_date')
	else:
		if selected_subject == None:
			items = Item.objects.filter(is_private=False).order_by('-pub_date')
		else:
			items = Item.objects.filter(is_private=False,subject=selected_subject).order_by('-pub_date')
	
	#all subjects
	subjects = Subject.objects.all()
	return render_to_response('items/items.html', {'subjects': subjects, 'items': items, 'selected_subject': selected_subject, 'type': type}, context_instance=RequestContext(request))

@login_required
def vote(request, id, vote):
	item = get_object_or_404(Item, id=id)
	xhr = request.GET.has_key('xhr')
	
	if item and RatingUsers.objects.filter(item=item,user=request.user).count() == 0:
		if vote == "up":
			item.rating = item.rating + 1
		if vote == "down":
			item.rating = item.rating - 1
		
		item.save()
		ru = RatingUsers(item=item, user=request.user)
		ru.save()
		
	if xhr:
		return HttpResponse(item.rating)
	
	return HttpResponseRedirect('/')

@login_required
def show(request, id):
	item = get_object_or_404(Item, id=id)
	
	if item.is_private == True:
		raise Http404
	
	#all subjects
	subjects = Subject.objects.all()
	
	comments = item.comments.all().order_by('-pub_date')
	
	return render_to_response('items/show.html', {'item': item, 'subjects': subjects, 'comments': comments}, context_instance=RequestContext(request))

@login_required
def comment(request):
	if 'item' in request.POST and is_number(request.POST['item']) and 'bbcode' in request.POST:
		item = get_object_or_404(Item, id=request.POST['item'])
		
		c = Comment(author = request.user, comment = request.POST['bbcode'])
		c.save()
		
		item.comments.add(c)
		item.save()
		
		return HttpResponseRedirect('/item/' + str(item.id))
	
	return HttpResponseRedirect('/')

@login_required
def download(request, id):
	serve = False
	redirect = '/'
	
	try:
		item = Item.objects.get(id=id)
	
		if item.is_private == True:
			redirect = '/my-files'
			
			if item.user == request.user:
				#serve private file to the user
				serve = True
		else:
			serve = True
			
		if serve:
			wrapper = FileWrapper(file(settings.FILES_URL + '/' + item.path))
			
			response = HttpResponse(wrapper, mimetype='application/force-download')
			response['Content-Disposition'] = 'attachment; filename=%s' % item.name
			#response['X-Sendfile'] = smart_str(path_to_file)
			
			return response
			
	except:
		None
	
	return HttpResponseRedirect(redirect)

@login_required
def delete(request, id):
	try:
		item = Item.objects.get(id=id)
	
		if item and item.user == request.user and item.is_private == True:
			os.remove(settings.FILES_URL + '/' + item.path)
			item.delete()
	except:
		None
	
	return HttpResponseRedirect('/my-files')
	
@login_required
def upload(request):
	if request.method == 'POST':
		ex = 's'
		try:
			name = request.FILES['file'].name
			ext = name.split('.')[len(name.split('.'))-1].lower()
			
			if request.POST['type'] != 'snov' and request.POST['type'] != 'vaja':
				raise CustomException("Wrong type")
			
			randomString = random_string(100) #random number just for kicks (it should be as random and unique as possible)
			i = Item(name = request.FILES['file'].name, content_type = request.FILES['file'].content_type, random_string = randomString, description = request.POST['description'], user = request.user, type = request.POST['type'], subject = Subject.objects.get(id=request.POST['subject']))
			
			if 'private' in request.POST:
				i.is_private = True
			
			i.save() #save it to get id
			
			code = str(i.id) + random_string(6)
			
			handle_uploaded_file(request.FILES['file'], code)
			
			i.path = code
			
			i.published = True
			i.save()
			
			if i.is_private == True:
				return HttpResponseRedirect('/my-files')
			else:
				return HttpResponseRedirect('/')
		except:
			#revert db/fs - delete created folder/file and remove DB entry
			
			try:
				if len(code) > 0:
					os.remove(settings.FILES_URL + '/' + code)
			except:
				#there might be a problem with removing folder/file
				None
			
			#try removing entry from DB
			try:
				i = Item.objects.get(random_string=randomString, published=False)
				i.delete()
			except:
				#entry not found, apparently we didn't create one therefore we don't need to remove folder/file
				None
			
			if 'private' in request.POST and request.POST['private'] == True:
				return HttpResponseRedirect('/my-files')
			else:
				return HttpResponseRedirect('/')

#Error 404 & 500
def error404(request):
	t = loader.get_template('items/error404.html')
	return HttpResponseNotFound(t.render(RequestContext(request, {})))