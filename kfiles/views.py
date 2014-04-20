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
from forms import UploadFileForm
from models import File_Upload

@login_required
def index(request):
	return render_to_response('index.html',{}, RequestContext(request))

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

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			instance = ModelWithFileField(file_field=request.FILES['file'])
			instance.save()
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})
