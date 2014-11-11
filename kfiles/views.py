from django.conf import settings
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext, Template
from django.template.defaultfilters import slugify

from models import *

def index(request):
	page_text = Page_Text.objects.get(page="index")
	rendered_text = page_text.render(RequestContext(request))
	return render_to_response('index.html',{'page_text':rendered_text}, RequestContext(request))

def password_reset(request, is_admin_site=False, template_name='password_reset_form.html', email_template_name='password_reset_email.html', password_reset_form=PasswordResetForm, token_generator=default_token_generator,post_reset_redirect=None):
	if post_reset_redirect is None: post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
	if request.method == 'GET' and request.GET.get('email',None):
		form = password_reset_form(initial={'email':request.GET.get('email')})
	elif request.method == "POST":
		form = password_reset_form(request.POST)
		if form.is_valid():
			opts = {}
			opts['use_https'] = request.is_secure()
			opts['token_generator'] = token_generator
			if is_admin_site:
				opts['domain_override'] = request.META['HTTP_HOST']
			else:
				opts['email_template_name'] = email_template_name
				if not Site._meta.installed:
					opts['domain_override'] = RequestSite(request).domain
			form.save(**opts)
			return HttpResponseRedirect(post_reset_redirect)
	else:
		form = password_reset_form()
	return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

def users(request):
	users = []
	for u in User.objects.all():
		p = Project_User.objects.filter(user=u).count()
		f = File_Upload.objects.filter(user=u).count()
		users.append((u,p,f))
	return render_to_response('users.html',{'users':users}, RequestContext(request))

@login_required
def projects(request):
	page_message = None
	if 'project_name' in request.POST:
		project_name = request.POST.get('project_name')
		project_slug = slugify(project_name)
		if Project.objects.filter(slug=project_slug):
			page_message = "That project name is taken."
		else:
			Project.objects.create(name=project_name, slug=project_slug)
	if request.user.is_staff: 
		projects = Project.objects.all()
	else:
		# This should be only the projects accesable by the user
		projects = Project.objects.all()
	return render_to_response('projects.html',{'page_message':page_message, 'projects':projects}, RequestContext(request))

@login_required
def project_view(request, project_slug):
	page_message = None
	project = get_object_or_404(Project, slug=project_slug)
	if request.user.is_staff: 
		files = File_Upload.objects.filter(project=project)
	else:
		files = File_Upload.objects.filter(project=project, user = request.user)
	project_users = None
	if request.user.is_staff: 
		project_users = Project_User.objects.filter(project=project)
		
	if 'file' in request.FILES:
		try:
			file=request.FILES['file']
			upload = File_Upload(user=request.user, project=project, 
				file=file, name=file.name, content_type=file.content_type)
			upload.save()
		except:
			page_message = "Could not save file"
	return render_to_response('project_view.html',{'page_message':page_message, 'project':project, 'files':files, 'project_users':project_users}, RequestContext(request))

@login_required
def project_users(request, project_slug):
	page_message = None
	project = get_object_or_404(Project, slug=project_slug)
	if 'emails' in request.POST:
		print "adding users: %s" % request.POST['emails']
		try:
			for email in request.POST['emails'].split(','):
				email = email.strip()
				user_search = User.objects.filter(email=email)
				if not user_search:
					user = User(username=email, email=email)
					user.save()
				else:
					user = user_search[0]
				pu = Project_User.objects.filter(project=project, user=user)
				if not pu:
					pu = Project_User(project=project, user=user)
					pu.save()
		except:
			page_message = "Could not add users"
	return render_to_response('project_view.html',{'page_message':page_message, 'project':project}, RequestContext(request))

@login_required
def user_view(request, user_id):
	page_message = None
	user = get_object_or_404(User, id=user_id)
	files = File_Upload.objects.filter(user=user).order_by('uploadTS')
	return render_to_response('user_view.html',{'page_message':page_message, 'user':user, 'files':files}, RequestContext(request))

@login_required
def file_download(request, project_slug, file_name):
	if not request.user.is_staff: 
		return HttpResponseRedirect(reverse('kfiles.views.project_view', kwargs={'page_message':'You do not have permission to download files', 'project_slug':project_slug}))
	project = get_object_or_404(Project, slug=project_slug)
	file_upload = File_Upload.objects.get(project=project, name=file_name)
	response = HttpResponse(file_upload.file, content_type=file_upload.content_type)
	response['Content-Disposition'] = 'attachment; filename="%s"' % file_upload.name
	return response
