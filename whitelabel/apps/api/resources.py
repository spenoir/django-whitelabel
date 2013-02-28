import logging
from django.conf import settings
from django.core.cache import cache
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from apps.pages.models import WebPage, GalleryImage

logger = logging.getLogger(__name__)

class UIdevAuthentication(Authentication):
    """ Override Tastypie Authentication and do a simple check for user role.
    The internal API is available to ADMIN and SUPERADMIN users only
    """

    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()

    def get_identifier(self, request):
        return request.user


class UIdevAuthorization(Authorization):
    """ Override Tastypie Authentication and do a simple check for user role.
    The internal API is available to ADMIN and SUPERADMIN users only
    """

    def is_authorized(self, request, object=None):
        return request.user.has_perm('page.view_api_page')


class ModelResourceBase(ModelResource):
    """ Base class for resources. Enables us to
    easily set common properties like auth and caching """

    class Meta:
        #authentication = UIdevAuthentication()
        #authorization = UIdevAuthorization()
        api_name = "uidev"
        filters_to_lowercase = []

    def get_list_json(self, request, **kwargs):
        try:
            modified_request = request
            modified_request_get = request.GET.copy()
            if modified_request_get.get('order_by'):
                modified_request_get.pop('order_by')
            modified_request_get.update({'format': 'json'})
            if kwargs:
                modified_request_get.update(kwargs)
        except AttributeError, e:
            #logger.log('Cannot process requests without GET vars, error was: %s' % e)
            return False

        modified_request.GET = modified_request_get

        cache_key = 'OBJECT_LIST_JSON-%s' % self.__class__.__name__
        try:
            # try to get the resource json from cache
            cached_resource_request = cache.get(cache_key)
            logger.log('Cache hit: %s' % cache_key)
            return cached_resource_request
        except:
            # otherwise set and get the cache
            cache.set(cache_key, self.get_list(request),
                settings.PAGE_CACHE_TIME)

            return cache.get(cache_key)


class PageResource(ModelResourceBase):

    class Meta(ModelResourceBase.Meta):
        queryset = WebPage.objects.all()


class GalleryImageResource(ModelResourceBase):

    class Meta(ModelResourceBase.Meta):
        queryset = GalleryImage.objects.all().order_by('date')
        ordering = ['date']

    def dehydrate(self, bundle):
        # set the artwork detail url
        bundle.data.setdefault('tags', [tag.name for tag in bundle.obj.tags.all()])

        return bundle
