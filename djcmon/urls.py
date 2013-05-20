from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from djauth.views import loggedout

urlpatterns = patterns('djcmon.views',
    # auth
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='auth_login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/communications/accounts/loggedout/'}),
    url(r'^accounts/loggedout/$', loggedout, {'template_name': 'accounts/logged_out.html'}),
    # core
    url(r'^$', 'home', name='comms_home'),
    url(r'^newsletters/$', 'home', name='newsletters_home'),
    url(r'^newsletters/manager/$', 'manager', name='newsletters_manager'),
    #url(r'^newsletters/unsubscribed/$', TemplateView.as_view(template_name="")),
    url(r'^newsletters/(?P<action>[\d\w]+)/$', 'subscription', name='subscription'),
)
