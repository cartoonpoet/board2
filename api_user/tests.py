from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


# Create your tests here.
class UserTests(APITestCase):
    def test_create_group(self):
        url = '/user/group/'
        data = {'group': '1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_account(self):
    #     url = ''
    #     data = {'id': 'testcase1', 'password': 'testcase1', 'name': 'testcase', 'group': '1', 'pw_check': 'testcase1'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(User.objects.get().name, 'testcase')
