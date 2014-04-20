from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
	url(r'^favicon.ico*$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'kfiles.views.index', name='home'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),	
	url(r'^reset/$', 'kfiles.views.password_reset', {'template_name': 'password_reset_form.html', 'email_template_name':'email/password_reset_email.txt'}),
	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}),
	url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}),
	url(r'^reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}),
	
)
