from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.conf import settings

from apps.pages.models import WebPage
from apps.api.resources import PageResource


def addvars(request):
    """ Make some extras vars available to all templates. """
    extra_vars = {}
    if hasattr(settings, 'APP_TITLE_SHORT'):
        extra_vars['APP_TITLE_SHORT'] = settings.APP_TITLE_SHORT
    if hasattr(settings, 'OFFLINE'):
        extra_vars['OFFLINE'] = settings.OFFLINE
    if hasattr(settings, 'TEMPLATE_CACHE_TIMEOUT'):
        extra_vars['TEMPLATE_CACHE_TIMEOUT'] = settings.TEMPLATE_CACHE_TIMEOUT
    if hasattr(settings, 'GOOGLE_ANALYTICS_KEY'):
        extra_vars['GOOGLE_ANALYTICS_KEY'] = settings.GOOGLE_ANALYTICS_KEY
    if hasattr(settings, 'DEBUG'):
        extra_vars['DEBUG'] = settings.DEBUG
    if hasattr(settings, 'SITE_ID'):
        extra_vars['SITE'] = Site.objects.get(id=settings.SITE_ID)

    if hasattr(settings, 'JS_GLOBAL_VARS'):
        settings.JS_GLOBAL_VARS.setdefault('API_URL', reverse('api_uidev_top_level', args=['uidev']))
        settings.JS_GLOBAL_VARS.setdefault('DEBUG', settings.DEBUG)
        extra_vars['JS_GLOBAL_VARS'] = simplejson.dumps(settings.JS_GLOBAL_VARS)

    pages_json = PageResource()

    extra_vars['pages_json'] = getattr(pages_json.get_list_json(request), 'content', {})

    return extra_vars


def menu_items(request):

    mainnav_pages = sorted(WebPage.objects.filter(live=True, main_nav=True).order_by('weight'),
        key=lambda l: l.slug =='blog')

    menu_items = {
        'topnav_pages': WebPage.objects.filter(live=True, top_nav=True).order_by('weight'),
        'mainnav_pages':mainnav_pages,
        'footer_pages': WebPage.objects.filter(live=True, footer_nav=True).order_by('weight')
    }

    return menu_items