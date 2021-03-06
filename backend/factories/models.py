from django.db import models
from django.conf import settings


class FactoryType(models.Model):
    name = models.CharField(max_length=100)
    human_name = models.CharField(max_length=100)
    description = models.TextField()
    base_production_rate = models.IntegerField(default=0)
    build_cost = models.IntegerField(default=0)
    base_upkeep_cost = models.IntegerField(default=0)
    level_upkeep_factor = models.DecimalField(decimal_places=1, max_digits=4)
    level_production_factor = models.DecimalField(decimal_places=1, max_digits=4)

    class Meta:
        db_table = "factories_factory_types"


class FactoryState(models.Model):
    name = models.CharField(max_length=100)
    human_name = models.CharField(max_length=255)

    class Meta:
        db_table = "factories_factory_states"


class Factory(models.Model):
    name = models.CharField(max_length=250, null=True)
    type = models.ForeignKey(FactoryType, on_delete=models.PROTECT)
    level = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    selling_price = models.DecimalField(decimal_places=2, max_digits=16, default=0.0)
    is_for_sale = models.BooleanField(default=True)
    price_per_unit = models.IntegerField(default=0)
    production_rate = models.IntegerField(default=0)
    units_stored = models.IntegerField(default=0)
    upkeep_cost = models.IntegerField(default=0)
    state = models.ForeignKey(FactoryState, on_delete=models.CASCADE)
    is_selling = models.BooleanField(default=False)

    class Meta:
        db_table = "factories_factories"
