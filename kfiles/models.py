from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.template import RequestContext, Template

class Project(models.Model):
	createdTS = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=60)

	def __unicode__(self):
	   return self.name

class Project_User(models.Model):
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

class Page_Text(models.Model):
	page = models.CharField(max_length=128)
	text_template = models.TextField(blank=True, null=True)
	def __unicode__(self):
		return self.page

	def render(self, context):
		template = Template(self.text_template)
		rendered = template.render(context)
		return rendered
