from django.test import TestCase
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class SnippetAddTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='nerd')
        self.code = 'ps -ef|grep grep'
        self.snippet1 = Snippet(code=self.code, owner=user)
        self.code = 'sudo nmap -p 8000'
        self.snippet2 = Snippet(code=self.code, owner=user)

    def test_add_snippet(self):
        old_object_count = Snippet.objects.count()
        self.snippet1.save()
        new_object_count = Snippet.objects.count()
        self.assertNotEqual(old_object_count, new_object_count)
        self.snippet2.save()
        newer_object_count = Snippet.objects.count()
        self.assertNotEqual(new_object_count, newer_object_count)


class SnippetViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='nerd')
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.snippet_data = {'code': 'asdfasdf', 'created': '2018-01-29T11:45', 'owner': user.id}
        self.response = self.client.post(reverse('list_or_create'), self.snippet_data, format='json')

    def test_api_can_create_a_snippet(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        new_client = APIClient()
        response = new_client.get('/snippets/', kwargs={'pk': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_a_snippet(self):
        snippet = Snippet.objects.get()
        response = self.client.get(reverse('update_or_delete', kwargs={'pk': snippet.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, snippet)

    def test_api_can_update_snippet(self):
        """Test the api can update a given bucketlist."""
        change_snippet = {'code': 'Something new', 'created': '2018-01-29T11:45'}
        res = self.client.put(
            reverse('update_or_delete', kwargs={'pk': Snippet.objects.get().id}),
            change_snippet, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, change_snippet['code'])

    def test_api_can_delete_snippet(self):
        old_object_count = Snippet.objects.count()
        response = self.client.delete(reverse('update_or_delete', kwargs={'pk': Snippet.objects.get().id}),
                                      format='json')
        new_object_count = Snippet.objects.count()
        self.assertEqual(old_object_count, new_object_count + 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
