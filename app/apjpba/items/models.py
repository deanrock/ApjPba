from django.db import models
from django.contrib.auth.models import User
from djangoratings.fields import RatingField

class Subject(models.Model):
	name = models.CharField(max_length=50)

class Comment(models.Model):
    author     = models.ForeignKey(User)
    comment   = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, null=False)
	published = models.BooleanField(default=False)
	path = models.CharField(max_length=200)
	pub_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	is_private = models.BooleanField(default=False)
	description = models.TextField(null=True, blank=True)
	subject = models.ForeignKey(Subject, null=False)
	type = models.CharField(max_length=100)
	content_type = models.CharField(max_length=100)
	random_string = models.CharField(max_length=200,null=True, blank=True)
	comments = models.ManyToManyField(Comment)
	
	#thumbs up & down
	rating = models.IntegerField(max_length=200,default=0)
	
	def __unicode__(self):
		return self.name

class RatingUsers(models.Model):
	item = models.ForeignKey(Item)
	user = models.ForeignKey(User)