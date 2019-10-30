from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import User
from django.core import management


class AccountTestCase(APITestCase):
    access_token = ''

    def setUp(self):
        management.call_command('seed_test')

        user = User.objects.create(pk=1, email='user@test.com', is_active=True)
        user.set_password('12qwaszx')
        user.save()
        url = reverse('token_obtain_pair')
        data = {'email': 'user@test.com', 'password': '12qwaszx'}
        response = self.client.post(url, data, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_fetch_account_data(self):
        url = reverse('account-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['email'], 'user@test.com')
        self.assertEqual(response.data['cash_total'], 30000000)
