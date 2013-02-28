from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from nose.tools import raises
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
#from johnny import cache as johnny_cache
from milkman.dairy import milkman
from django.test import TestCase

from apps.pages.models import WebPage


class TestWebPageModel(TestCase):

    def setUp(self):
        settings.TEST = True

        cache.clear()
   #     johnny_cache.disable()

        self.page = milkman.deliver(WebPage, slug='test-page', title="Test page")
        self.user = User.objects.create_user(username='user',
            email='email@example.com', password='pass')
        self.client.login(username='user', password='pass')

    def test_new_page_renders(self):
        response = self.client.get(reverse('webpage_view', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)

    @raises(ValidationError)
    def test_page_slug_error(self):
        milkman.deliver(WebPage, base_template="pages/page_detail.html",
            slug="@WE3e$%???>><$%^<script>", title="blooddy ell")

    def test_page_slug(self):
        milkman.deliver(WebPage, base_template="pages/page_detail.html",
            slug="page-slug_is_good", title="innit maaaate")
        self.assertIsInstance(WebPage.objects.get(slug='page-slug_is_good'), WebPage)

    @raises(ValidationError)
    def test_page_slug_unique(self):
        milkman.deliver(WebPage, base_template="pages/page_detail.html",
            slug="page-slug_is_good", title="this is a good un")
        milkman.deliver(WebPage, template="pages/page_detail.html", slug="page-slug_is_good")

    def test_home_page_creation(self):
        "Test that the homepage slug is empty and not 'home'"
        homepage = milkman.deliver(WebPage, title='Home')
        self.assertFalse(homepage.slug)

    def test_no_template(self):
        page = milkman.deliver(WebPage, slug='notemplate', title="no template")
        response = self.client.get(reverse('webpage_view', args=[page.slug]))
        self.assertEqual(page.base_template, 'base/page_detail.html')
        self.assertEqual(page.template, 'pages/default.html')
        self.assertEqual(response.status_code, 200)

    def test_decimal_weight(self):
        page = milkman.deliver(WebPage, slug='decimal-page', title="decimal weight",
            weight="0.2")
        response = self.client.get(reverse('webpage_view', args=[page.slug]))
        self.assertTrue(page)
        self.assertEqual(response.status_code, 200)

