from django.db import models


# Create your models here.
class Session(models.Model):
    class Meta:
        db_table = 'sessions'
    
    session_name    = models.CharField(max_length=250)
    session_data = models.TextField()
    last_check = models.DateTimeField()
    
