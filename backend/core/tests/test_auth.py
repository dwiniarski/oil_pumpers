from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import User
from time import gmtime, strftime


class RegistrationTestCase(APITestCase):
    def setUp(self):
        pass

    def test_user_can_register_and_activate(self):
        user_email = 'dummy.user@test.com'
        date_format = '%Y-%m-%d'

        url_register = reverse('register')
        data = {'email': user_email, 'password': 'secret1940', 'password_confirm': 'secret1940'}
        response = self.client.post(url_register, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email=user_email)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.date_joined.strftime(date_format), strftime(date_format, gmtime()))
        self.assertEqual(len(user.activation_token), 32)

        url_activate = reverse('activate', kwargs={'activation_token': user.activation_token})
        response = self.client.get(url_activate, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email=user_email)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.activation_token, '')


class ActivationTestCase(APITestCase):
    def setUp(self):
        pass

    def test_user_cant_activate_account_with_wrong_token(self):
        url_register = reverse('register')
        data = {'email': 'user@test.com', 'password': '12qwaszx'}
        self.client.post(url_register, data, format='json')

        url_activate = reverse('activate', kwargs={'activation_token': 'gsflonj4t3gtonlngsoigf4ngoasngff'})
        response = self.client.get(url_activate, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    def setUp(self):
        user_active = User.objects.create(email='active@test.com', is_active=True)
        user_active.set_password('12qwaszx')
        user_active.save()

        user_inactive = User.objects.create(email='inactive@test.com', is_active=False)
        user_inactive.set_password('12qwaszx')
        user_inactive.save()

    def test_successful_login(self):
        url = reverse('token_obtain_pair')
        data = {'email': 'active@test.com', 'password': '12qwaszx'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    def test_inactive_login_try(self):
        url = reverse('token_obtain_pair')
        data = {'email': 'inactive@test.com', 'password': '12qwaszx'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_password_given(self):
        url = reverse('token_obtain_pair')
        data = {'email': 'active@test.com', 'password': 'wrong_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
