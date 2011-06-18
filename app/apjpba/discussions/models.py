from django.db import models
from django.contrib.auth.models import User
import datetime

class Post(models.Model):
	post = models.TextField()
	user = models.ForeignKey(User, null=False)
	pub_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

class Topic(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, null=False)
	pub_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(null=True) #date of last post
	modified_user = models.ForeignKey(User, null=True, related_name = 'modified_by_user_set') #last post's user
	posts = models.ManyToManyField(Post)
	
	#mark topic as read for current user
	def mark_as_read(self, user):
		try:
			lv = LastView.objects.filter(user=user,topic=self)[0]
			lv.date = datetime.datetime.now()
			lv.save()
		except:
			lv = LastView(user=user, date=datetime.datetime.now(), topic=self)
			lv.save()
	
	def get_last_visit(self, user):
		try:
			last_view = LastView.objects.get(topic=self,user=user).date
			
			return last_view
		except:
			return None
	
	def has_new_posts(self, user):
		try:
			last_view = LastView.objects.get(topic=self,user=user).date
			
			if self.modified_date > last_view:
				return True
			else:
				return False
		
		except:
			return True #there is no record of last visit of the topic by selected user

class LastView(models.Model):
	user = models.ForeignKey(User, null=False)
	date = models.DateTimeField(auto_now=True)
	topic = models.ForeignKey(Topic, null=False)
	
	unique_together = (( "user", "topic", ),)