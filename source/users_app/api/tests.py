from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .views import UserViewSet


User = get_user_model()

# Create your tests here.
class UserAPITests(TestCase):

    def setUp(self):

        self.client = APIClient()

    @staticmethod
    def create_users():
        users = []
        for i in range(1, 11):
            users.append(User(username=f"test_user{i}", email=f"test_user{i}@example.com", password="testpassword"))

        User.objects.bulk_create(users)

    def test_user_api_resolves_to_UserAPIViewSet(self):

        # this view is used in GET and POST requests
        view = resolve(reverse("user-list"))

        self.assertEqual(view.func.__name__, UserViewSet.__name__)

        # this view is used in GET, PUT, PATCH and DELETE requests
        view = resolve(reverse("user-detail", kwargs={"pk": 1}))

        self.assertEqual(view.func.__name__, UserViewSet.__name__)

    def test_list_users(self):

        self.create_users()

        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(User.objects.all(), many=True).data)

    def test_get_user_by_id(self):

        User.objects.create(username='test_user', email='test_user@example.com', password="testpassword")

        response = self.client.get(reverse("user-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(User.objects.get(pk=1)).data)

    def test_create_user(self):

        payload = {"username": "test_user", "email": "test_user@example.com", "password": "testpassword"}
        response = self.client.post(reverse("user-list"), data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), UserSerializer(User.objects.get(pk=1)).data)

    def test_update_user(self):

        User.objects.create(username='test_user', email='test_user@example.com', password="testpassword")

        payload = {"username": "new_username", "email": "new_username@example.com", "password": "testpassword"}
        response = self.client.put(reverse("user-detail", kwargs={"pk": 1}), data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(User.objects.get(pk=1)).data)

    def test_patch_user(self):

        User.objects.create(username='test_user', email='test_user@example.com', password="testpassword")

        payload = {"username": "new_username", "email": "new_username@example.com"}
        response = self.client.patch(reverse("user-detail", kwargs={"pk": 1}), data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(User.objects.get(pk=1)).data)

    def test_delete_user(self):

        User.objects.create(username='test_user', email='test_user@example.com', password="testpassword")

        response = self.client.delete(reverse("user-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(),0)
