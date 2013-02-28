import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils.decorators import classonlymethod
from django.views.decorators.cache import cache_page

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView

from apps.pages.models import WebPage, GalleryImage
from apps.api.resources import GalleryImageResource
from apps.pages.forms import ContactForm

logger = logging.getLogger(__name__)

handler404 = TemplateView.as_view(template_name="404.html")
handler500 = TemplateView.as_view(template_name="500.html")


class BasePageContextMixin(object):
    " adds specific page rendering items to context amongst other things "

    def get_context_data(self, **kwargs):
        context = super(BasePageContextMixin, self).get_context_data(**kwargs)


        extra_context = {
            'slug': self.kwargs.get('slug'),
#            'basket': self.basket
        }
        #extra_context.update(self.basket.cart_totals(self.request))
        context.update(extra_context)
        return context


class BasePageView(BasePageContextMixin, UpdateView):
    " Base view for basic pages "
    context_object_name = 'page'
    template_name = 'pages/default.html'

    def get_template_names(self):
        names = super(BasePageView, self).get_template_names()

        tpl = getattr(self.object, 'base_template')
        if tpl:
            names.reverse()
            names.append(tpl)
            names.reverse()

        return names

    def get_object(self, queryset=None):
        # fix for homepage slug ie. no slug

        if not self.kwargs.get('slug') and self.model == WebPage:
            # return the home page
            try:
                return self.model.objects.get(slug='', live=True)
            except self.model.DoesNotExist:
                page, created = self.model.objects.get_or_create(
                    slug='', title='Home', template='pages/default.html')

                return page

        return self.model.objects.get(slug=self.kwargs.get('slug'), live=True)

    def get(self, request, **kwargs):
        response = super(BasePageView, self).get(request, **kwargs)
#        self.basket = Basket(request)

        return response

    def post(self, request, *args, **kwargs):
        response = super(BasePageView, self).post(request, **kwargs)
#        self.basket = Basket(request)

        return response
#        return HttpResponse('Unauthorized', status=401)

    def get_context_data(self, **kwargs):
        context = super(BasePageView, self).get_context_data(**kwargs)

        # get the next or previous and update context
        context.update(self.get_next_and_prev())
        return context

    def get_next_and_prev(self, *args, **kwargs):
        # this method is intended to get the next and previous WebPage
        # by weight
        try:
            next_pages = self.model.objects.filter(weight__gt=self.object.weight) \
                    .order_by('weight')
            prev_pages = self.model.objects.filter(weight__lt=self.object.weight) \
                    .order_by('-weight')

            return {
                'next': next_pages[0] if next_pages.count() else False,
                'prev': prev_pages[0] if prev_pages.count() else False
            }
        except:
            logging.debug('No next and previous pages found for: %s' % self)
            return {
                'next': False,
                'prev': False
            }

    @classonlymethod
    def as_view(cls, **initkwargs):
        """ Specialised so we can cache view. """
        view = super(BasePageView, cls).as_view(**initkwargs)
        cached_view = cache_page(
            view, settings.PAGE_CACHE_TIME,
            key_prefix=settings.CACHE_KEY_PREFIX)

        logger.debug('called BasePageview.as_view() DEBUG: %s and CACHE_PAGES: %s' % (settings.DEBUG, settings.CACHE_PAGES))

        if not settings.DEBUG and settings.CACHE_PAGES:
            return cached_view
        else:
            return view


class WebPageView(BasePageView):
    model = WebPage

webpage_view = WebPageView.as_view()


class ContactFormView(BasePageContextMixin, FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_mail(fail_silently=False)
        return super(ContactFormView, self).form_valid(form)

contact_form_view = ContactFormView.as_view()


class GalleryPageView(BasePageView):
    model = WebPage

    def get_context_data(self, **kwargs):
        context = super(GalleryPageView, self).get_context_data(**kwargs)

        gallery_images_json = GalleryImageResource()

        context.update({
            'gallery_images': GalleryImage.objects.filter(live=True).order_by('-date'),
            'gallery_images_json': gallery_images_json.get_list_json(self.request, order_by='-date').content
        })

        return context

gallerypage_view = GalleryPageView.as_view()

class HomePageView(BasePageView):
    model = WebPage

homepage_view = HomePageView.as_view()


class ClearCache(BasePageContextMixin, TemplateView):
    template_name = 'utils/clear_cache.html'

    def get(self, request, *args, **kwargs):
        from johnny.localstore import LocalStore
        store = LocalStore()
        store.clear()
        
        cache.clear()

        return super(ClearCache, self).get(request, *args, **kwargs)

clear_cache = login_required(ClearCache.as_view())