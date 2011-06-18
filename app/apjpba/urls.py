from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

handler404 = 'apjpba.items.views.error404'
handler500 = 'apjpba.items.views.error404'

urlpatterns = patterns('',
	#Items
	(r'^files$', 'apjpba.items.views.index', {'type': ''}),
	(r'^my-files$', 'apjpba.items.views.index', {'type': 'my-files'}),
	(r'^upload$', 'apjpba.items.views.upload'),
	(r'^delete/(.*)$', 'apjpba.items.views.delete'),
	(r'^download/(.*)$', 'apjpba.items.views.download'),
	(r'^vote/(.*)/(.*)$', 'apjpba.items.views.vote'),
	(r'^item/(.*)$', 'apjpba.items.views.show'),
	(r'^comment$', 'apjpba.items.views.comment'),
	
	#Discussions
	(r'^discussions$', 'apjpba.discussions.views.index'),
	(r'^discussions/topic/(.*)$', 'apjpba.discussions.views.show'),
	(r'^discussions/new-topic$', 'apjpba.discussions.views.new_topic'),
	(r'^discussions/new-post$', 'apjpba.discussions.views.new_post'),
	
	#Answers
	(r'^$', 'apjpba.answers.views.index'),
	(r'^question$', 'apjpba.answers.views.show_answer'),
	(r'^answers/edit/(.*)$', 'apjpba.answers.views.edit'),
	(r'^answers/version/(.*)$', 'apjpba.answers.views.version'),
	
    # Example:
    # (r'^apjpba/', include('apjpba.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    #Users
	(r'^login', 'apjpba.users.views.fbmoodle_login'),
	#(r'^fbmoodle_login$', 'apjpba.users.views.fbmoodle_login'),
	(r'^channel.html', 'apjpba.users.views.fbchannel'),
	(r'^fblogin$', 'apjpba.users.views.fblogin'),
	(r'^logout$', 'apjpba.users.views.logout'),
	#(r'^register$', 'apjpba.users.views.register'),
	(r'^user/(.*)$', 'apjpba.users.views.show'),
	#(r'^reset-password$', 'apjpba.users.views.reset_password'),
	
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^stylesheets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT+'/stylesheets'}),
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT+'/images'}),
        (r'^javascripts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT+'/javascripts'}),
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FILES_URL}),
    )