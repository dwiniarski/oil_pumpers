from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import User
from django.core import management
from core.models import OilField


class OilFieldTestCase(APITestCase):
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

        # seed some oil fields
        OilField.objects.create(pk=1, required_drilling_depth=4082, volume_starting=74743467,
                                volume_left=74743467, selling_price=5134418)
        OilField.objects.create(pk=2, required_drilling_depth=1011, volume_starting=148943672,
                                volume_left=148943672, selling_price=19566335)
        OilField.objects.create(pk=3, required_drilling_depth=3173, volume_starting=135934516,
                                volume_left=135934516, selling_price=11859592)
        OilField.objects.create(pk=4, required_drilling_depth=750, volume_starting=137077391,
                                volume_left=137077391, selling_price=18737640)
        OilField.objects.create(pk=5, required_drilling_depth=2887, volume_starting=833123,
                                volume_left=833123, selling_price=77548)

    def test_list_oil_fields_for_sale(self):
        url = reverse('list-oil-fields-for-sale')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buy_oil_field(self):
        oil_field_id = 3
        url = reverse('buy-oil-field', kwargs={'pk': oil_field_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=1)
        self.assertEqual(user.cash_total, 18140408)
        oil_field = OilField.objects.get(pk=oil_field_id)
        self.assertEqual(oil_field.owner, user)
        self.assertEqual(oil_field.is_for_sale, False)

    def test_set_oil_field_for_sale(self):
        oil_field_id = 4
        oil_field_selling_price = 150000
        user = User.objects.get(pk=1)
        oil_field = OilField.objects.get(pk=oil_field_id)
        oil_field.owner = user
        oil_field.is_for_sale = False
        oil_field.save()
        url = reverse('set-for-sale-oil-field', kwargs={'pk': oil_field_id})
        data = {'price': oil_field_selling_price}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        oil_field = OilField.objects.get(pk=oil_field_id)
        self.assertEqual(oil_field.is_for_sale, True)
        self.assertEqual(oil_field.selling_price, oil_field_selling_price)
