from rest_framework import serializers
from core.models import User, OilField, OilFieldStatus
from core.mail import send_activation_email
from core.enums import OilFieldStatusEnum


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        password_confirm = data.get('password_confirm', None)

        users = User.objects.filter(email=email)
        if len(users) > 0:
            raise serializers.ValidationError(
                {'email': 'User with this email already exists in a database!'})

        if password != password_confirm:
            raise serializers.ValidationError(
                {'password_confirm': 'Password and password confirmation are not the same!'})

        return {
            'email': data.get('email', None),
            'password': password
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_email(user)
        return user


class ActivationSerializer(serializers.Serializer):
    activation_token = serializers.CharField(min_length=32, max_length=32)

    def validate_activation_token(self, value):
        user = User.objects.filter(activation_token=value)
        if len(user) != 1:
            raise serializers.ValidationError('Activation code could not be validated.')
        return value

    def save(self):
        user = User.objects.get(activation_token=self.validated_data['activation_token'])
        user.is_active = True
        user.activation_token = ''
        user.save()


class OilFieldStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilFieldStatus
        fields = '__all__'


class OilFieldSerializer(serializers.ModelSerializer):
    status = OilFieldStatusSerializer()

    class Meta:
        model = OilField
        exclude = ['required_drilling_depth', 'volume_starting', 'volume_left']


class OilFieldBuySerializer(serializers.Serializer):
    oil_field_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        oil_field_id = data.get('oil_field_id', None)
        user_id = data.get('user_id', None)

        oil_field = OilField.objects.filter(is_for_sale=True, pk=oil_field_id).first()
        if not oil_field:
            raise serializers.ValidationError(
                'Oil field does not exist or is not for sale.'
            )
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        if user.cash_total < oil_field.selling_price:
            raise serializers.ValidationError('User does not have enough money to buy this oil field.')

        return {
            'oil_field_id': oil_field_id,
            'user_id': user_id
        }

    def save(self):
        user = User.objects.get(pk=self.validated_data.get('user_id'))
        oil_field = OilField.objects.get(pk=self.validated_data.get('oil_field_id'))
        user.cash_total = user.cash_total - oil_field.selling_price
        user.save()
        oil_field.is_for_sale = False
        oil_field.owner = user
        oil_field.save()


class OilFieldStartDrillingSerializer(serializers.Serializer):
    oil_field_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        oil_field_id = data.get('oil_field_id', None)
        user_id = data.get('user_id', None)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        oil_field = OilField.objects.filter(pk=oil_field_id).first()
        if not oil_field:
            raise serializers.ValidationError('Oil field does not exist.')

        if oil_field.owner != user:
            raise serializers.ValidationError('This oil field does not belong to you.')

        if oil_field.status_id != OilFieldStatusEnum.IDLE.value:
            raise serializers.ValidationError('The oil field state must be idle before starting drilling.')

        if not oil_field.amount_drills > 0:
            raise serializers.ValidationError('You have no drills to start drilling.')

        return {
            'oil_field_id': oil_field_id,
            'user_id': user_id
        }

    def save(self):
        oil_field = OilField.objects.get(pk=self.validated_data.get('oil_field_id'))
        oil_field.status_id = OilFieldStatusEnum.DRILLING.value
        oil_field.save()


class OilFieldStopDrillingSerializer(serializers.Serializer):
    oil_field_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        oil_field_id = data.get('oil_field_id', None)
        user_id = data.get('user_id', None)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        oil_field = OilField.objects.filter(pk=oil_field_id).first()
        if not oil_field:
            raise serializers.ValidationError('Oil field does not exist.')

        if oil_field.owner != user:
            raise serializers.ValidationError('This oil field does not belong to you.')

        if oil_field.status_id != OilFieldStatusEnum.DRILLING.value:
            raise serializers.ValidationError('The oil field must be drilling if you want to stop drilling.')

        return {
            'oil_field_id': oil_field_id,
            'user_id': user_id
        }

    def save(self):
        oil_field = OilField.objects.get(pk=self.validated_data.get('oil_field_id'))
        oil_field.status_id = OilFieldStatusEnum.IDLE.value
        oil_field.save()


class OilFieldSetForSaleSerializer(serializers.Serializer):
    oil_field_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    price = serializers.IntegerField()

    def validate(self, data):
        oil_field_id = data.get('oil_field_id', None)
        user_id = data.get('user_id', None)
        price = data.get('price', None)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        oil_field = OilField.objects.filter(is_for_sale=False, pk=oil_field_id, owner=user).first()
        if not oil_field:
            raise serializers.ValidationError(
                'Oil field does not exist, is for sale or does not belong to this user.'
            )

        if price <= 0:
            raise serializers.ValidationError(
                'Price has to be greater than 0.'
            )

        return {
            'oil_field_id': oil_field_id,
            'user_id': user_id,
            'price': price
        }

    def save(self):
        oil_field = OilField.objects.get(pk=self.validated_data.get('oil_field_id'))
        oil_field.is_for_sale = True
        oil_field.selling_price = self.validated_data.get('price')
        oil_field.save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'is_active', 'activation_token']
