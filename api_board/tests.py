from django.test import TestCase
from django.urls import reverse
from django.http import QueryDict
from rest_framework import status
from rest_framework.test import APITestCase
from api_user.models import User, Group, User_Group
from .models import Board


# Create your tests here.
class BoardTests(APITestCase):
    def setUp(self):
        Group.objects.create(id=1)
        Group.objects.create(id=2)
        User.objects.create(id='test', password='test', name='test')
        User_Group.objects.create(user_id_id='test', group_id_id='1')

    def write_post(self):
        url = reverse('api_board:board_API')
        data = QueryDict('title=post&contents=write&user=test')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().title, 'post')

    def modify_post(self):
        url = reverse('api_board:board_API', kwargs={'post_num': '1'})
        data = QueryDict('title=수정&contents=수정&user=test')
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Board.objects.get().title, '수정')

    def get_all_post(self):
        url = reverse('api_board:board_API')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_one_post(self):
        url = reverse('api_board:board_API', kwargs={'post_num': '1'})
        data = {'viewer': 'test'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_post(self):
        url = reverse('api_board:board_API', kwargs={'post_num': '1'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Board.objects.count(), 0)

    def test_board(self):
        self.write_post()
        self.modify_post()
        self.get_all_post()
        self.get_one_post()
        self.delete_post()
