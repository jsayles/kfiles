from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext, Template

@login_required
def index(request):
	return render_to_response('index.html',{}, RequestContext(request))

	from django.http import HttpResponseRedirect
	from django.shortcuts import render
	from .forms import UploadFileForm
	from .models import ModelWithFileField

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
