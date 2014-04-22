from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings

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

	def files(self):
		return File_Upload.objects.filter(project=self)

	def members(self):
		return Project_Member.objects.filter(project=self)

	def __unicode__(self):
	   return self.name

class Project_Member(models.Model):
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, blank=True, null=True, unique=False)

	def __unicode__(self):
	   return "%s - %s" % (self.project, self.user)

class File_Upload(models.Model):
	uploadTS = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, blank=False)
	name = models.CharField(max_length=64)
	content_type = models.CharField(max_length=64)
	file = models.FileField(upload_to=settings.DATA_DIR, blank=False)

	def __unicode__(self):
	   return self.file.name
