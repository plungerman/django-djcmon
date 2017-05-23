from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from djauth.views import loggedout

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

from djcmon import views

urlpatterns = [
    # auth
    url(
        r'^accounts/login/$',
        auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',
        auth_views.logout,
        {'next_page': '/communications/accounts/loggedout/'},
        name="auth_logout"
    ),
    url(
        r'^accounts/loggedout/$',
        loggedout,
        {'template_name': 'accounts/logged_out.html'}
    ),
    #url(
    #   r'^saml2/', include('djangosaml2.urls')
    #),
    #url(
    #   r'^saml-test/$',
    #   'saml_test',
    #   name='saml_test'
    #),
    # core
    url(
        r'^$', views.home, name='comms_home'
    ),
    url(
        r'^newsletters/$',
        views.home,
        name='newsletters_home'
    ),
    url(
        r'^newsletters/manager/$',
        views.manager,
        name='newsletters_manager'
    ),
    #url(
    #    r'^newsletters/unsubscribed/$',
    #    TemplateView.as_view(template_name="")
    #),
    url(
        r'^newsletters/(?P<action>[\d\w]+)/$',
        views.subscription,
        name='subscription'
    ),
]
'''
urlpatterns += [
    url(
        r'^test/', 'djangosaml2.views.echo_attributes'
    ),
]
'''
