from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=255,null=True)
    created_date = models.DateTimeField(null=True,blank=True,max_length=255)

    

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    created_date = models.DateTimeField(null=True,blank=True,max_length=255)
    updated_date = models.DateTimeField(null=True,blank=True,max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
