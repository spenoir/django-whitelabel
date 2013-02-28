from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.utils import simplejson
from milkman.dairy import milkman
import os
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.api.resources import PageResource
from apps.pages.models import WebPage


class ApiTest(TestCase):

    def setUp(self):
        self.api_page_json = os.path.join(self.get_api_url('page'), '?format=json')
        self.page = milkman.deliver(WebPage, slug='test-page', title='Test page')

    def get_api_url(self, resource_name):
        return reverse('api_dispatch_list', kwargs={'resource_name': resource_name, 'api_name': 'uidev'})

    def test_api_url(self):
        response = self.client.get(self.get_api_url('page'))
        self.assertEqual(response.status_code, 200)

    def test_page_json(self):
        response = self.client.get(self.api_page_json)
        json = simplejson.loads(response.content)

        test_page = {}
        for obj in json.get('objects'):
            if obj.get('slug') == 'test-page':
                test_page = obj

        self.assertTrue(test_page)


class ApiResourceTest(TestCase):

    def setUp(self):
        self.page = milkman.deliver(WebPage, slug='test-page', title="page", template='pages/default.html')
        self.page2 = milkman.deliver(WebPage, slug='test-page-2', title="page2", template='pages/default.html')
        self.page_resource = PageResource()
        self.user = User.objects.create_user(username='user', email='email@example.com', password='pass')
        self.client.login(username='user', password='pass')

        self.rf = RequestFactory()


    def test_get_list_json(self):
        request = self.rf.get('/test-page/')
        response = self.page_resource.get_list_json(request)
        self.assertEqual(response.status_code, 200)

    def test_get_list_json_response(self):
        request = self.rf.get('/test-page-2/')
        response = self.page_resource.get_list_json(request)
        self.assertTrue('objects' in simplejson.loads(response.content).keys())