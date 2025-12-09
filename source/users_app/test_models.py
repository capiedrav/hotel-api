from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser, UserProfile
from django.db.utils import IntegrityError


User = get_user_model()


class UserModelTests(TestCase):

    def setUp(self):

        self.payload = {"email": 'test_user@example.com', "password": 'testpassword'}

    @staticmethod
    def create_user(user_data: dict[str, str]) -> User:

        return User.objects.create_user(**user_data)

    def test_user_model_is_CustomUser(self):

        self.assertEqual(CustomUser, User)

    def test_create_user(self):

        self.create_user(self.payload)

        self.assertEqual(User.objects.count(), 1)

        user = CustomUser.objects.get(pk=1)
        self.assertEqual(user.email, self.payload['email'])
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_cant_create_user_without_email(self):

        with self.assertRaises(ValueError):
            self.create_user({"email": "", "password": "testpassword"})

        self.assertEqual(User.objects.count(), 0)

    def test_create_superuser(self):

        User.objects.create_superuser(**self.payload)

        self.assertEqual(User.objects.count(), 1)

        superuser = User.objects.get(pk=1)

        self.assertEqual(superuser.email, self.payload['email'])
        self.assertTrue(superuser.check_password(self.payload["password"]))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_cant_create_superuser_without_email(self):

        with self.assertRaises(ValueError):
            User.objects.create_superuser(**{"email": "", "password": "testpassword"})

        self.assertEqual(User.objects.count(), 0)

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

    def test_email_is_unique(self):

        self.create_user(self.payload) # create a user

        with self.assertRaises(IntegrityError):
            self.create_user(self.payload) # try to create a user with the same email

        # self.assertEqual(User.objects.count(), 1)