from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    class Meta:
        db_table = 'categories'
    
    name = models.CharField(max_length=250)

class Question(models.Model):
    class Meta:
        db_table = 'questions'
    
    category = models.ForeignKey(Category, null=False, db_column='category')
    question = models.TextField()

class File(models.Model):
    class Meta:
        db_table = 'files'
    
    question = models.ForeignKey(Question, null=False, db_column='question')
    user = models.ForeignKey(User, null=False, db_column='user')
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=250)
    size = models.IntegerField()
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=250)
    hidden = models.BooleanField(default=False)
    
class Content(models.Model):
    class Meta:
        db_table = 'content'
    
    type = models.CharField(max_length=100)
    question = models.ForeignKey(Question, null=False, db_column='question')
    user = models.ForeignKey(User, null=False, db_column='user')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

