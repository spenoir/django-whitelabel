from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
#from johnny import cache as johnny_cache
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from milkman.dairy import milkman

from apps.pages.models import WebPage
from nose.tools import raises


class TestPageViews(TestCase):

    def setUp(self):
        settings.TEST = True

        cache.clear()
       # johnny_cache.disable()

        self.page = milkman.deliver(WebPage, slug='test-page', title='Test page',
            base_template="pages/page_detail.html", main_nav=True, weight=30)

        self.user = User.objects.create_user(username='user',
            email='email@example.com', password='pass')
        self.client.login(username='user', password='pass')

    def test_new_page_renders(self):
        response = self.client.get(reverse('webpage_view', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)

    def test_home_page(self):
        response = self.client.get(reverse('home'))

        self.assertTrue(response.status_code, 200)

    @raises(ValidationError)
    def test_bad_html_content(self):
        html = open(os.path.join(settings.DJANGO_ROOT, 'apps', 'pages', 'tests',
                        'disallowed_tags.html')).read()
        new_page = milkman.deliver(WebPage, slug='new-page', content=html, title='New page')
        self.assertEqual(type(WebPage.objects.get(slug='new-page').content), unicode)

    def test_good_html_content(self):
        html = open(os.path.join(settings.DJANGO_ROOT, 'apps', 'pages', 'tests',
                        'allowed_tags.html')).read()
        new_page = milkman.deliver(WebPage, slug='new-page', content=html, title='New page')
        self.assertEqual(type(WebPage.objects.get(slug='new-page').content), unicode)


    def tearDown(self):
        self.client.logout()