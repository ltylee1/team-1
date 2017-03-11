from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.test import Client
from django.core.urlresolvers import reverse

# class UserProfileTest(TestCase):
#     def setUp(self):
#         User.objects.create_user('john', password='password')
#
#     def test_create_user_create_profile(self):
#         self.assertTrue(Profile.objects.filter(user__username = 'john').exists())
#
#     def test_delete_user_delete_profile(self):
#         User.objects.get(username = 'john').delete()
#         self.assertFalse(Profile.objects.filter(user__username='john').exists())


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        self.client = Client()

    def test_login(self):
        # login
        response = self.client.post(reverse('login'), **self.credentials)

        # should be logged in now, fails however
        user = User.objects.get(username = response.request["username"])
        self.assertTrue(user.is_authenticated)

    def test_incorrect_password(self):
        # login
        response = self.client.post(reverse('login'), username = 'testuser', password = 'incorrect')

        # should be logged in now, fails however
        print list(response.context)
        user = User.objects.get(username = response.request["username"])
        self.assertFalse(user.is_authenticated)

