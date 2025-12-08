from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser, UserProfile
from django.forms.models import model_to_dict


User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):

        self.payload = {"username": 'test_user', "email": 'test_user@example.com', "password": 'testpassword'}

    @staticmethod
    def create_user(user_data: dict) -> User:

        return User.objects.create(**user_data)

    def test_user_model_is_CustomUser(self):

        self.assertEqual(CustomUser, User)

    def test_create_user(self):

        user = self.create_user(self.payload)

        self.assertEqual(User.objects.count(), 1)
        self.assertDictEqual(model_to_dict(user, fields=["username", "email", "password"]), self.payload)

    def test_user_profile_is_created_when_user_is_created(self):

        user = self.create_user(self.payload)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.first().user, user)

    def test_delete_user_also_deletes_user_profile(self):

        # create a user
        user = self.create_user(self.payload)

        # check the user profile is created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

        # delete the user
        user.delete()

        # and check the user profile is also deleted
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
