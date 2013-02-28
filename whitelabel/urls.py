import os
from django.conf import settings
from django.contrib import admin, sitemaps
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import GenericSitemap
from apps.pages.models import WebPage

admin.autodiscover()

info_dict = {
    'queryset': WebPage.objects.all(),
    'date_field': 'pub_date',
    }

sitemaps = {
    'blog': GenericSitemap(info_dict, priority=0.6),
    }


urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # static media
    url(r'^media(?P<path>.*)$', 'django.views.static.serve',
        {'document_root' : settings.MEDIA_ROOT}),

    # uploads dir
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root' : os.path.join(settings.SITE_ROOT, 'uploads')}),


    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    url(r'^comments/', include('django.contrib.comments.urls')),

    (r'^ckeditor/', include('ckeditor.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login_view'),

    (r'^api/', include('apps.api.urls')),

    (r'^', include('apps.pages.urls')),
)
