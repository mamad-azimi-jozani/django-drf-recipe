"""
test for user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(user.email, payload['email'])
        self.assertNotIn('password', res.data)

    def test_user_with_email_exist_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'pass123',
            'name': 'Test'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_errors(self):
        payload = {
            'email': 'test@example.com',
            'password': 'pass',
            'name': 'Test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        user_detail = {
            'name': 'test_token',
            'email': 'token@gmail.com',
            'password': 'token-pass123'
        }
        create_user(**user_detail)

        payload = {
            'email': user_detail['email'],
            'password': user_detail['password']
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        user_detail = {
            'name': 'test_token',
            'email': 'token@gmail.com',
            'password': 'token-pass123'
        }
        create_user(**user_detail)

        payload = {
            'email': '',
            'password': 'bad-pass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_blank_password(self):
        user_detail = {
            'name': 'test_token',
            'email': 'token@gmail.com',
            'password': 'token-pass123'
        }
        create_user(**user_detail)
        payload = {
            'email': 'test@gmail.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



