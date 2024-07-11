from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):

    def test_register(self):
        # get data
        # send data get response
        # check response status code
        data = {
            "username": "testuser",
            "email": "abdelrahman.hassan.hamdy@gmail.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        reverse_url = reverse("register")
        response = self.client.post(reverse_url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "abdelrahman.hassan.hamdy@gmail.com")


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("obtain-token")
        self.logout_url = reverse("logout")
        self.user_data = {
            "username": "testuser",
            "email": "abdelrahman.hassan.hamdy@gmail.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        self.user = User.objects.create_user(username="testuser2", password="testpassword")
        self.login_data = {
                "username": "testuser2",
                "password": "testpassword",
            }

    def test_login_register_new_user(self):
        # register
        self.client.post(self.register_url, self.user_data)
        # login
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.token = response.data["token"]

    def test_login_created_user(self):
        # login
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue("token" in response.data)

    def test_logout(self):
        # login
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.token = response.data["token"]
        print(self.token)
        # we can get the token directly from the user object
        # self.token = Token.objects.get(user__username="testuser2").key
        # logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, HTTP_200_OK)
