from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import User
from django.core import management
from factories.enums import FactoryTypeEnum, FactoryStateEnum
from factories.models import Factory, FactoryType, FactoryState


class FactoriesTestCase(APITestCase):
    access_token = ''
    user = ''

    def setUp(self):
        management.call_command('seed_test')

        self.user = User.objects.create(pk=1, email='user@test.com', is_active=True)
        self.user.set_password('12qwaszx')
        self.user.save()
        url = reverse('token_obtain_pair')
        data = {'email': 'user@test.com', 'password': '12qwaszx'}
        response = self.client.post(url, data, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_found_factory(self):
        # Let's build a pump factory
        url = reverse('build-factory')
        data = {'factory_type_id': FactoryTypeEnum.PUMP_FACTORY.value, 'name': 'The Great Pump Factory'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=1)
        self.assertEqual(user.cash_total, 16000000)
        try:
            factory = Factory.objects.get(owner=user, type_id=FactoryTypeEnum.PUMP_FACTORY.value)
        except factory.DoesNotExist:
            self.fail()
        self.assertEqual(factory.level, 1)
        self.assertEqual(factory.is_for_sale, False)
        self.assertEqual(factory.state.id, FactoryStateEnum.NON_OPERATIONAL.value)
        self.assertEqual(factory.is_selling, False)

    def test_toggle_operational_factory(self):
        factory_type = FactoryType.objects.get(pk=FactoryTypeEnum.PUMP_FACTORY.value)
        factory_state_non_operational = FactoryState.objects.get(pk=FactoryStateEnum.NON_OPERATIONAL.value)
        factory_state_operational = FactoryState.objects.get(pk=FactoryStateEnum.OPERATIONAL.value)
        factory = Factory.objects.create(pk=1, name='The Great Pump Factory', level=1, price_per_unit=0,
                                         production_rate=factory_type.base_production_rate, units_stored=0,
                                         upkeep_cost=factory_type.base_upkeep_cost, owner=self.user, type=factory_type,
                                         is_for_sale=False, state=factory_state_non_operational)
        url = reverse('toggle-operational-factory', kwargs={'pk': factory.id})
        response = self.client.post(url, format='json')
        factory = Factory.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(factory.state, factory_state_operational)

        response = self.client.post(url, format='json')
        factory = Factory.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(factory.state, factory_state_non_operational)

    def test_upgrade_factory(self):
        pass
