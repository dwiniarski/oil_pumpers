from django.core.management.base import BaseCommand
from core.models import OilField, OilFieldStatus
from factories.models import FactoryType, FactoryState
from core import config
from core.enums import OilFieldStatusEnum
from factories.enums import FactoryTypeEnum, FactoryStateEnum
import random


class SeedCommand(BaseCommand):
    help = 'Populates database with data'

    def populate_oil_field_status(self):
        for status in OilFieldStatusEnum:
            OilFieldStatus.objects.create(pk=status.value, name=status.name)

    def generate_oil_fields(self):
        for i in range(1, config.NUMBER_OF_OIL_FIELDS):
            required_drilling_depth = random.randint(config.MIN_DRILLING_DEPTH, config.MAX_DRILLING_DEPTH)
            total_volume = random.randint(config.MIN_VOLUME, config.MAX_VOLUME)  # barrels
            selling_price = 0.1 * total_volume * ((1 / (-4900)) * required_drilling_depth + 1.52)
            selling_price = round(selling_price)
            OilField.objects.create(required_drilling_depth=required_drilling_depth, volume_starting=total_volume,
                                    volume_left=total_volume, selling_price=selling_price)

    def populate_factory_types(self):
        FactoryType.objects.create(pk=FactoryTypeEnum.DRILL_FACTORY.value,
                                   name=FactoryTypeEnum.DRILL_FACTORY.name,
                                   human_name="Drill factory",
                                   description="You need drills to drill a hole to the oil.",
                                   base_production_rate=config.DRILL_FACTORY_BASE_PRODUCTION_RATE,
                                   base_upkeep_cost=config.DRILL_FACTORY_BASE_UPKEEP_COST,
                                   build_cost=config.DRILL_FACTORY_BUILD_COST)
        FactoryType.objects.create(pk=FactoryTypeEnum.PUMP_FACTORY.value,
                                   name=FactoryTypeEnum.PUMP_FACTORY.name,
                                   human_name="Pump factory",
                                   description="Pumps are used to get the oil to the ground",
                                   base_production_rate=config.PUMP_FACTORY_BASE_PRODUCTION_RATE,
                                   base_upkeep_cost=config.PUMP_FACTORY_BASE_UPKEEP_COST,
                                   build_cost=config.PUMP_FACTORY_BUILD_COST)
        FactoryType.objects.create(pk=FactoryTypeEnum.PIPE_FACTORY.value,
                                   name=FactoryTypeEnum.PIPE_FACTORY.name,
                                   human_name="Pipe factory",
                                   description="You need pipes to pump the oil to the surface.",
                                   base_production_rate=config.PIPE_FACTORY_BASE_PRODUCTION_RATE,
                                   base_upkeep_cost=config.PIPE_FACTORY_BASE_UPKEEP_COST,
                                   build_cost=config.PIPE_FACTORY_BUILD_COST)
        FactoryType.objects.create(pk=FactoryTypeEnum.WAGON_FACTORY.value,
                                   name=FactoryTypeEnum.WAGON_FACTORY.name,
                                   human_name="Wagon factory",
                                   description="Wagon are needed to transport the oil to the buyer.",
                                   base_production_rate=config.WAGON_FACTORY_BASE_PRODUCTION_RATE,
                                   base_upkeep_cost=config.WAGON_FACTORY_BASE_UPKEEP_COST,
                                   build_cost=config.WAGON_FACTORY_BUILD_COST)
        FactoryType.objects.create(pk=FactoryTypeEnum.STORAGE_TANK_FACTORY.value,
                                   name=FactoryTypeEnum.STORAGE_TANK_FACTORY.name,
                                   human_name="Storage tank factory",
                                   description="Storage tanks are used to store oil extracted to the ground.",
                                   base_production_rate=config.STORAGE_TANK_FACTORY_BASE_PRODUCTION_RATE,
                                   base_upkeep_cost=config.STORAGE_TANK_FACTORY_BASE_UPKEEP_COST,
                                   build_cost=config.STORAGE_TANK_FACTORY_BUILD_COST)

    def populate_factory_states(self):
        FactoryState.objects.create(pk=FactoryStateEnum.NON_OPERATIONAL.value,
                                    name=FactoryStateEnum.NON_OPERATIONAL.name, human_name='Non operational')
        FactoryState.objects.create(pk=FactoryStateEnum.OPERATIONAL.value,
                                    name=FactoryStateEnum.OPERATIONAL.name, human_name='Operational')

    def handle(self, *args, **options):
        pass


class Command(SeedCommand):
    def handle(self, *args, **options):
        self.populate_oil_field_status()
        self.generate_oil_fields()
        self.populate_factory_types()
        self.populate_factory_states()
