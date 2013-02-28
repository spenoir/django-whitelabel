from django.conf.urls import patterns, url, include

from tastypie.api import Api
from .resources import PageResource, GalleryImageResource

v1_api = Api(api_name='uidev')
v1_api.register(PageResource())
v1_api.register(GalleryImageResource())

urlpatterns = patterns('',
    url(r'^', include(v1_api.urls)),
)