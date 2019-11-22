from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import User
from django.core import management
from core.models import OilField
from core.enums import OilFieldStatusEnum


class OilFieldTestCase(APITestCase):
    access_token = ''
    user = ''
    another_user = ''
    oil_fields = ''

    def setUp(self):
        management.call_command('seed_test')

        self.user = User.objects.create(pk=1, email='user@test.com', is_active=True)
        self.user.set_password('12qwaszx')
        self.user.save()

        # creating another user
        self.another_user = User.objects.create(pk=2, email='another@test.com', is_active=True)
        self.another_user.set_password('12qwaszx')
        self.another_user.save()

        url = reverse('token_obtain_pair')
        data = {'email': 'user@test.com', 'password': '12qwaszx'}
        response = self.client.post(url, data, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.oil_fields = list()

        # seed some oil fields
        self.oil_fields.append(OilField.objects.create(pk=1, required_drilling_depth=4082, volume_starting=74743467,
                                                       volume_left=74743467, selling_price=5134418))
        self.oil_fields.append(OilField.objects.create(pk=2, required_drilling_depth=1011, volume_starting=148943672,
                                                       volume_left=148943672, selling_price=19566335))
        self.oil_fields.append(OilField.objects.create(pk=3, required_drilling_depth=3173, volume_starting=135934516,
                                                       volume_left=135934516, selling_price=11859592))
        self.oil_fields.append(OilField.objects.create(pk=4, required_drilling_depth=750, volume_starting=137077391,
                                                       volume_left=137077391, selling_price=18737640))
        self.oil_fields.append(OilField.objects.create(pk=5, required_drilling_depth=2887, volume_starting=833123,
                                                       volume_left=833123, selling_price=77548))

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
        url = reverse('oil-field-detail', kwargs={'pk': oil_field_id})
        data = {'id': oil_field_id, 'selling_price': oil_field_selling_price, 'is_for_sale': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        oil_field = OilField.objects.get(pk=oil_field_id)
        self.assertEqual(oil_field.is_for_sale, True)
        self.assertEqual(oil_field.selling_price, oil_field_selling_price)

    def test_list_my_oil_fields(self):
        self.oil_fields[1].owner = self.user
        self.oil_fields[1].save()
        self.oil_fields[3].owner = self.user
        self.oil_fields[3].save()
        self.oil_fields[4].owner = self.user
        self.oil_fields[4].save()
        url = reverse('account-oil-fields')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_start_drilling_without_drills(self):
        oil_field_id = 4
        oil_field = OilField.objects.get(pk=oil_field_id)
        oil_field.owner = self.user
        oil_field.save()
        url = reverse('start-drilling', kwargs={'pk': oil_field_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'You have no drills to start drilling.')

    def test_start_drilling_with_drills(self):
        oil_field_id = 4
        oil_field = OilField.objects.get(pk=oil_field_id)
        oil_field.owner = self.user
        oil_field.amount_drills = 50
        oil_field.save()
        url = reverse('start-drilling', kwargs={'pk': oil_field_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        oil_field = OilField.objects.get(pk=oil_field_id)
        self.assertEqual(oil_field.status_id, OilFieldStatusEnum.DRILLING.value)

    def test_start_drilling_another_users_oil_field(self):
        oil_field_id = 4
        oil_field = OilField.objects.get(pk=oil_field_id)
        oil_field.owner = self.another_user
        oil_field.save()
        url = reverse('start-drilling', kwargs={'pk': oil_field_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stop_drilling(self):
        oil_field_id = 4
        oil_field = OilField.objects.get(pk=oil_field_id)
        oil_field.owner = self.user
        oil_field.status_id = OilFieldStatusEnum.DRILLING.value
        oil_field.save()
        url = reverse('stop-drilling', kwargs={'pk': oil_field_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        oil_field = OilField.objects.get(pk=oil_field_id)
        self.assertEqual(oil_field.status_id, OilFieldStatusEnum.IDLE.value)

    def test_stop_drilling_another_users_oil_field(self):
        oil_field_id = 4
        oil_field = OilField.objects.get(pk=oil_field_id)
        oil_field.owner = self.another_user
        oil_field.status_id = OilFieldStatusEnum.DRILLING.value
        oil_field.save()
        url = reverse('stop-drilling', kwargs={'pk': oil_field_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
