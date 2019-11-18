from django.core.management.base import BaseCommand
from factories.models import Factory
from django.db import transaction


class Command(BaseCommand):
    help = 'Update factories production and upkeep'

    @transaction.atomic
    def handle(self, *args, **options):
        factories = Factory.objects.all()
        for factory in factories:
            factory.units_stored = factory.units_stored + factory.production_rate
            factory.save()
            factory.owner.cash_total = factory.owner.cash_total - factory.upkeep_cost
            factory.owner.save()
