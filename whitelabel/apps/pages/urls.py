from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from apps.pages.views import homepage_view, webpage_view,\
    contact_form_view, gallerypage_view, clear_cache


urlpatterns = patterns('',

    # redirect home slug
    url(r'^home/$', RedirectView.as_view(url='/')),

    url(r'^clear-cache/', clear_cache, name='clear_cache'),

    url(r'^contact/$', contact_form_view, name='contact_form_view'),
    url(r'^(?P<slug>(gallery))/$', gallerypage_view, name='gallerypage_view'),
    url(r'^(?P<slug>[\w\-]+)/$', webpage_view, name='webpage_view'),

    url(r'^$', homepage_view, name='home'),

)
