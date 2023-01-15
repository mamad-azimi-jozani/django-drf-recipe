"""
test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models

class ModelTests(TestCase):
    """ test models """

    def test_create_user_with_email_successful(self):
        email = 'uesr@egample.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,

        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalize(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'password123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'password123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'password123',

        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):

        user = get_user_model().objects.create(
            email='test@gmail.com',
            password='test12345',
            name='test',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='sample description'
        )

        self.assertEqual(str(recipe), recipe.title)