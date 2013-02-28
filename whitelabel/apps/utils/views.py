# Create your views here.
import logging
import os
from django.conf import settings
from django.views.generic.base import RedirectView


class StaticRedirectView(RedirectView):
    url = settings.STATIC_URL

    def get(self, request, *args, **kwargs):

        if self.kwargs.get('path') and not settings.DEBUG:
            self.url = os.path.join(settings.STATIC_URL, self.kwargs.get('path'))

        return super(StaticRedirectView, self).get(request, *args, **kwargs)

static_redirect = StaticRedirectView.as_view()