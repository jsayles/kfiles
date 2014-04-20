from django.db import models
from django.contrib.auth.models import User, Group

class ProjectManager(models.Manager):
	def files(self):
		return File_Upload.objects.filter(project=self)

	def members(self):
		return Project_Member.objects.filter(project=self)
		
class Project(models.Model):
	objects = ProjectManager()
	
	createdTS = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=60)

class Project_Member(models.Model):
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, blank=True, null=True, unique=False)

class File_Upload(models.Model):
	uploadTS = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, blank=True, null=True, unique=False)
	file = models.FileField()
