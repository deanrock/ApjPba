# coding=utf8
from django import template
from datetime import datetime
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

def bbcode(value):
	"""
    Generates (X)HTML from string with BBCode "markup".
    By using the postmark lib from:
    @see: http://code.google.com/p/postmarkup/
    
	""" 
	try:
		from postmarkup import render_bbcode
	except ImportError:
		if settings.DEBUG:
			raise template.TemplateSyntaxError, "Error in {% bbcode %} filter: The Python postmarkup library isn't installed."
		return force_unicode(value)
	else:
		return mark_safe(render_bbcode(value))
bbcode.is_save = True

@register.filter
def strip_bbcode(value):
	""" 
    Strips BBCode tags from a string
    By using the postmark lib from: 
    @see: http://code.google.com/p/postmarkup/
    
	""" 
	try:
		from postmarkup import strip_bbcode
	except ImportError:
		if settings.DEBUG:
			raise template.TemplateSyntaxError, "Error in {% bbcode %} filter: The Python postmarkup library isn't installed."
		return force_unicode(value)
	else:
		return mark_safe(strip_bbcode(value))
bbcode.is_save = True

def callMethod(obj, methodName):
    method = getattr(obj, methodName)

    if obj.__dict__.has_key("__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()

def args(obj, arg):
    if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []
    
    obj.__callArg += [arg]
    return obj
  
@register.filter 
def naturalTimeDifference(value):
	"""
	Finds the difference between the datetime value given and now()
	and returns appropriate humanize form
	"""
	
	if isinstance(value, datetime):
		delta = datetime.now() - value
		if delta.days > 6:
			return value.strftime("%b %d")                    # May 15
		if delta.days > 1:
			return value.strftime("%A")                       # Wednesday
		elif delta.days == 1:
			return u'včeraj'                                # yesterday
		elif delta.seconds > 3600:
			return diffToHours(delta.seconds/3600)
		elif delta.seconds >  60:
			return diffToMinutes(delta.seconds/60)
		else:
			return diffToSeconds(delta.seconds)
		
		return defaultfilters.date(value)
	else:
		return str(value)


def diffToMinutes(minutes):
	x = 'minutami'
	
	if minutes <= 1:
		x = 'minuto'
	elif minutes <= 2:
		x = 'minutama'
	return 'pred ' + str(minutes) + ' ' + x

def diffToSeconds(seconds):
	x = 'sekundami'
	
	if seconds <= 1:
		return 'pred 1 sekundo'
	elif seconds <= 2:
		x = 'sekundama'
	return 'pred ' + str(seconds) + ' ' + x

def diffToHours(hours):
	x = 'urami'
	
	if hours <= 1:
		x = 'uro'
	elif hours <= 2:
		x = 'urama'
	return 'pred ' + str(hours) + ' ' + x

def diffToDays(days):
	x = 'dnevi'
	
	if days <= 1:
		return u'včeraj'
	elif days <= 2:
		x = 'dnevoma'
	return 'pred ' + str(days) + ' ' + x

def show_items(items):
	return {'items': items}

def show_posts(posts):
	return {'posts': posts}

register.filter("call", callMethod)
register.filter("args", args)
register.inclusion_tag('tags/show_items.html')(show_items)
register.inclusion_tag('tags/show_posts.html')(show_posts)
register.filter("bbcode", bbcode)