from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from core.enums import OilFieldStatusEnum
from core.config import STARTING_CASH
from core.utils import generate_random_string


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if email is None:
            raise TypeError('User must have an email')
        if password is None:
            raise TypeError('User must have a password')

        user = self.model(email=email)
        user.set_password(password)
        user.is_active = False
        user.is_superuser = False
        user.is_staff = False
        user.activation_token = generate_random_string(32)
        user.save()

        return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    username = ''
    first_name = ''
    last_name = ''
    email = models.EmailField('email', blank=False, unique=True)
    cash_total = models.IntegerField(default=STARTING_CASH)
    activation_token = models.CharField(max_length=32, null=True)


class OilFieldStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "core_oil_field_status"


class OilField(models.Model):
    name = models.CharField(max_length=250, null=True)
    status = models.ForeignKey(OilFieldStatus, default=OilFieldStatusEnum.IDLE.value, on_delete=models.PROTECT)
    required_drilling_depth = models.IntegerField(null=False)
    volume_starting = models.IntegerField()
    volume_left = models.IntegerField()
    selling_price = models.PositiveIntegerField(default=0)
    is_for_sale = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    amount_drills = models.IntegerField(default=0)
    amount_pipes = models.IntegerField(default=0)
    amount_wagons = models.IntegerField(default=0)
    amount_storage_tanks = models.IntegerField(default=0)
    amount_pumps = models.IntegerField(default=0)
    storage_tank_max_capacity = models.IntegerField(default=0)
    storage_tank_consumed_capacity = models.IntegerField(default=0)
    current_drilling_depth = models.IntegerField(default=0)

    class Meta:
        db_table = "core_oil_fields"
