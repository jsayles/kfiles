from django.db import models
from django.contrib.auth.models import User, Group

class Project(models.Model):
	name = models.CharField(max_length=200)
	createdTS = models.DateTimeField(auto_now_add=True)
	slug = models.CharField(max_length=60)

class Project_Member(models.Model):
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, blank=True, null=True, unique=False)

class File_Upload(models.Model):
	uploadTS = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, blank=True, null=True, unique=False)
	file_field = models.FileField()
