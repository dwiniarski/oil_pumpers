from core.management.commands.seed import SeedCommand


class Command(SeedCommand):
    def handle(self, *args, **options):
        self.populate_oil_field_status()
        self.populate_factory_types()
        self.populate_factory_states()
