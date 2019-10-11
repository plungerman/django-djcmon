from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path, reverse_lazy

from djauth.views import loggedout

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

from djcmon import views


urlpatterns = [
    # auth
    path(
        'accounts/login/', auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login'
    ),
    path(
        'accounts/logout/', auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout'
    ),
    path(
        'accounts/loggedout/', loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout'
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'), name='access_denied'
    ),
    # saml tests
    #path('saml2/', include('djangosaml2.urls')),
    #path('saml-test/', 'saml_test', name='saml_test'),
    # core
    path(
        '', views.home, name='comms_home'
    ),
    path(
        'newsletters/', views.home, name='newsletters_home'
    ),
    path(
        'newsletters/manager/', views.manager, name='newsletters_manager'
    ),
    #path(
    #    'newsletters/unsubscribed/', TemplateView.as_view(template_name="")
    #),
    re_path(
        r'^newsletters/(?P<action>[\d\w]+)/$', views.subscription,
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
