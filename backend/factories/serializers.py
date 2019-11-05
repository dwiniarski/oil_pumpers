from rest_framework import serializers
from core.models import User
from factories.models import FactoryType, Factory, FactoryState
from factories.enums import FactoryStateEnum


class FactoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryType
        fields = '__all__'


class FactoryBuildSerializer(serializers.Serializer):
    factory_type_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    name = serializers.CharField()

    def validate(self, data):
        factory_type_id = data.get('factory_type_id', None)
        user_id = data.get('user_id', None)
        name = data.get('name', None)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        try:
            factory_type = FactoryType.objects.get(pk=factory_type_id)
        except FactoryType.DoesNotExist:
            raise serializers.ValidationError(
                'Oil field does not exist, is for sale or does not belong to this user.'
            )

        if user.cash_total < factory_type.build_cost:
            raise serializers.ValidationError('User does not have enough money to buy this factory.')

        return {
            'factory_type_id': factory_type_id,
            'user_id': user_id,
            'name': name
        }

    def save(self):
        factory_type = FactoryType.objects.get(pk=self.validated_data.get('factory_type_id'))
        factory_state = FactoryState.objects.get(pk=FactoryStateEnum.NON_OPERATIONAL.value)
        user = User.objects.get(pk=self.validated_data.get('user_id'))
        Factory.objects.create(name=self.validated_data.get('name'), level=1, price_per_unit=0,
                               production_rate=factory_type.base_production_rate, units_stored=0,
                               upkeep_cost=factory_type.base_upkeep_cost, owner=user, type=factory_type,
                               is_for_sale=False, state=factory_state)
        user.cash_total = user.cash_total - factory_type.build_cost
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
