from rest_framework import serializers
from core.models import User
from core.serializers import UserSerializer
from factories.models import FactoryType, Factory, FactoryState
from factories.enums import FactoryStateEnum
from django.db import transaction


class FactoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryType
        fields = '__all__'


class FactoryStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryState
        fields = '__all__'


class FactorySerializer(serializers.ModelSerializer):
    state = FactoryStateSerializer()
    type = FactoryTypeSerializer()

    class Meta:
        model = Factory
        fields = '__all__'


class FactoryBuildSerializer(serializers.Serializer):
    factory_type_id = serializers.IntegerField()
    unit_price = serializers.IntegerField()
    name = serializers.CharField()
    start_production_when_build = serializers.BooleanField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        factory_type_id = data.get('factory_type_id')
        unit_price = data.get('unit_price')
        name = data.get('name', None)
        user_id = data.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        try:
            factory_type = FactoryType.objects.get(pk=factory_type_id)
        except FactoryType.DoesNotExist:
            raise serializers.ValidationError("Factory type does not exist.")

        if user.cash_total < factory_type.build_cost:
            raise serializers.ValidationError('User does not have enough money to buy this factory.')

        if unit_price <= 0:
            raise serializers.ValidationError('Unit price cannot smaller or equal to zero.')

        return {
            'factory_type_id': factory_type_id,
            'name': name,
            'unit_price': unit_price,
            'start_production_when_build': data.get('start_production_when_build'),
            'user_id': user_id
        }

    def save(self):
        user = User.objects.get(pk=self.validated_data.get('user_id'))
        factory_type = FactoryType.objects.get(pk=self.validated_data.get('factory_type_id'))
        if self.validated_data.get('start_production_when_build'):
            factory_state = FactoryState.objects.get(pk=FactoryStateEnum.OPERATIONAL.value)
        else:
            factory_state = FactoryState.objects.get(pk=FactoryStateEnum.NON_OPERATIONAL.value)

        Factory.objects.create(name=self.validated_data.get('name'), level=1,
                               price_per_unit=self.validated_data.get('unit_price'),
                               production_rate=factory_type.base_production_rate, units_stored=0,
                               upkeep_cost=factory_type.base_upkeep_cost, owner=user,
                               type=factory_type,
                               is_for_sale=False, state=factory_state)
        user.cash_total = user.cash_total - factory_type.build_cost
        user.save()


class FactoryUpgradeSerializer(serializers.Serializer):
    factory_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        factory_id = data.get('factory_id')
        user_id = data.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        try:
            if user.is_superuser:
                factory = Factory.objects.get(pk=factory_id)
            else:
                factory = Factory.objects.get(pk=factory_id, owner=user)
        except Factory.DoesNotExist:
            raise serializers.ValidationError("Factory type does not exist.")

        if user.cash_total < factory.type.build_cost:
            raise serializers.ValidationError('User does not have enough money to upgrade this factory.')

        return {
            'factory_id': factory_id,
            'user_id': user_id
        }

    @transaction.atomic
    def save(self):
        user = User.objects.get(pk=self.validated_data.get('user_id'))
        factory = Factory.objects.get(pk=self.validated_data.get('factory_id'))
        factory.level = factory.level + 1
        factory.production_rate = factory.production_rate * factory.type.level_production_factor
        factory.upkeep_cost = int(round(factory.upkeep_cost * factory.type.level_upkeep_factor))
        factory.save()

        user.cash_total = user.cash_total - factory.type.build_cost
        user.save()


class FactoryToggleOperationalSerializer(serializers.Serializer):
    factory_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        factory_id = data.get('factory_id', None)
        user_id = data.get('user_id', None)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        try:
            Factory.objects.get(pk=factory_id, owner=user)
        except Factory.DoesNotExist:
            raise serializers.ValidationError('Factory does not exist or does not belong to given user.')

        return {
            'factory_id': factory_id,
            'user_id': user_id
        }

    def save(self):
        user = User.objects.get(pk=self.validated_data['user_id'])
        factory = Factory.objects.get(pk=self.validated_data['factory_id'], owner=user)
        if factory.state.id == FactoryStateEnum.NON_OPERATIONAL.value:
            factory.state = FactoryState.objects.get(pk=FactoryStateEnum.OPERATIONAL.value)
        elif factory.state.id == FactoryStateEnum.OPERATIONAL.value:
            factory.state = FactoryState.objects.get(pk=FactoryStateEnum.NON_OPERATIONAL.value)

        factory.save()
