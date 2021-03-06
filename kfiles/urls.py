from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
	url(r'^favicon.ico*$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
	url(r'^admin/', include(admin.site.urls)),
	
	url(r'^$', 'kfiles.views.index', name='home'),
	url(r'^project/$', 'kfiles.views.projects', name='projects'),
	url(r'^project/(?P<project_slug>[^/]+)$', 'kfiles.views.project_view', name='project_view'),
	url(r'^project/(?P<project_slug>[^/]+)/(?P<file_name>[^/]+)$', 'kfiles.views.file_download', name='file_download'),
	url(r'^users/$', 'kfiles.views.users', name='users'),
	url(r'^users/(?P<project_slug>[^/]+)/$', 'kfiles.views.project_users', name='project_users'),
	url(r'^user/(?P<user_id>\d+)$', 'kfiles.views.user_view', name='user_view'),
	
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),	
	url(r'^reset/$', 'kfiles.views.password_reset', {'template_name': 'password_reset_form.html', 'email_template_name':'email/password_reset_email.txt'}),
	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}),
	url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}),
	url(r'^reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}),
)
