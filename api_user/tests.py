from django.test import TestCase
from django.urls import reverse
from django.http import QueryDict
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Group, User_Group


# Create your tests here.
class UserTests(APITestCase):
    def setUp(self):
        Group.objects.create(id=1)
        Group.objects.create(id=2)

    def create_account(self):
        url = '/user/'
        data = QueryDict('id=testcase&password=testcase&pw_check=testcase&group=1&name=testcase')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'testcase')

    def test1(self):
        self.assertEqual(Group.objects.count(), 2)
        self.create_account()