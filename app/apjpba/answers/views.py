# coding=utf8
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from apjpba.answers.models import Question, Category, Content, File
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
import string, random, os, sys
from django.utils import simplejson
import datetime, time
from django.conf import settings
from apjpba.utils import sanitizeHtml
from django.core.servers.basehttp import FileWrapper
from django.http import Http404

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

@login_required
def index(request):
    questions = []
    
    categories = Category.objects.all().order_by('id')
    
    i= 0
    for c in categories:
        i=i+1
        
        q = Question.objects.filter(category=c).order_by('id')
        o = {}
        o['category'] = c
        o['i'] = i
        o['questions'] = q
        
        j = 0
        for one in o['questions']:
            j=j+1
            one.j = j
        
        
        questions.append(o)
    
    #que2 = Struct(**questions)
    return render_to_response('answers/questions.html',
                               {'questions':questions}, 
                               context_instance=RequestContext(request))

@login_required
def show_answer(request):
    if 'id' in request.POST and 'div' in request.POST:
        id = request.POST['id']
        div = request.POST['div']
        
        question = Question.objects.get(id=id)
        
        if question:
            try:
                latest_answer = Content.objects.filter(question=question,type='answer').order_by('-id')[0]
            except:
                latest_answer = None
            
            try:
                latest_code = Content.objects.filter(question=question,type='code').order_by('-id')[0]
            except:
                latest_code = None
                
            #show files
            files = File.objects.filter(question=question, hidden=False).order_by('-id')
            
            files_pictures = []
            other_files = []
            allowed = ["image/png", "image/jpeg", "image/pjpeg", "image/jpg",  "image/gif"]
            
            for file in files:
                x = None
                
                for a in allowed:
                    if file.type == a:
                        x = file
                
                if x:
                    files_pictures.append(file)
                else:
                    other_files.append(file)
        
            return render_to_response('answers/show_answer.html',
                                  {'question': question, 'latest_answer': latest_answer,'latest_code': latest_code, 'div': div,
                                   'files_pictures': files_pictures, 'other_files':other_files},
                                  context_instance=RequestContext(request))
        else:
            return HttpResponse('Question doesn\'t exist')
    else:
        return HttpResponse('')

@login_required
def version(request, id):
   content = get_object_or_404(Content, id=id)
   
   question = content.question
   
   contents = Content.objects.filter(type=content.type,question=question).order_by('id')
   
   before_info = None
   after_info = None
   
   for c in contents:
       if c.id > content.id:
           after_info = c
           break
       elif c.id == content.id:
           pass
       else:
           before_info = c
   
   return render_to_response('answers/version.html',
                             {'content': content,
                              'question': question,
                              'before_info': before_info,
                              'after_info': after_info
                              },
                             context_instance = RequestContext(request))

@login_required
def edit(request, id):
    question = Question.objects.get(id=id)
    
    if question:
        try:
            latest_answer = Content.objects.filter(question=question,type='answer').order_by('-id')[0]
        except:
            latest_answer = None
            
        try:
            answer_changes = Content.objects.filter(question=question,type='answer').order_by('-id')
        except:
            answer_changes = None
        
        try:
            latest_code = Content.objects.filter(question=question,type='code').order_by('-id')[0]
        except:
            latest_code = None
            
        try:
            code_changes = Content.objects.filter(question=question,type='code').order_by('-id')
        except:
            code_changes = None
        
        if 'code' in request.POST:
            if latest_code:
                b = latest_code.content
            else:
                b = ''
            
            code = request.POST['code']
            code = code.replace('<', '&lt;')
            code = code.replace('>', '&gt;')
            code = sanitizeHtml(code)
            
            if code != b:
                #user changed code, add it to content
                c = Content(question=question, user=request.user, type='code')
                c.content = code
                c.save()
                return HttpResponseRedirect('/answers/edit/'+str(question.id))
        
        if 'answer' in request.POST:
            if latest_answer:
                b = latest_answer.content
            else:
                b = ''
                
            if sanitizeHtml(request.POST['answer']) != b:
                #user changed code, add it to content
                c = Content(question=question, user=request.user, type='answer')
                c.content = sanitizeHtml(request.POST['answer'])
                c.save()
                return HttpResponseRedirect('/answers/edit/'+str(question.id))
          
        #show files
        files = File.objects.filter(question=question, hidden=False).order_by('-id')
        
        #hidden files
        hidden_files = File.objects.filter(question=question, hidden=True).order_by('-id')
        
        files_pictures = []
        other_files = []
        allowed = ["image/png", "image/jpeg", "image/pjpeg", "image/jpg",  "image/gif"]
        
        for file in files:
            x = None
            
            for a in allowed:
                if file.type == a:
                    x = file
            
            if x:
                files_pictures.append(file)
            else:
                other_files.append(file)
                
        return render_to_response('answers/edit.html',
                                  {'question': question, 'latest_answer': latest_answer,'latest_code': latest_code,
                                   'files_pictures': files_pictures, 
                                   'other_files':other_files,
                                   'hidden_files': hidden_files,
                                   'answer_changes': answer_changes,
                                   'code_changes': code_changes},
                                  context_instance=RequestContext(request))