from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class UserProfileTest(TestCase):
    def setUp(self):
        User.objects.create_user('john', password='password')

    def test_create_user_create_profile(self):
        self.assertTrue(Profile.objects.filter(user__username = 'john').exists())

    def test_delete_user_delete_profile(self):
        User.objects.get(username = 'john').delete()
        self.assertFalse(Profile.objects.filter(user__username='john').exists())



