from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Deletes all migration files'

    def handle(self, *args, **options):
        print("Clering migrations...")
        apps = ('core', 'factories')
        for app in apps:
            init_file_path = os.path.join(os.getcwd(), app, 'migrations', '0001_initial.py')
            if os.path.exists(init_file_path):
                print("\t" + app + "...")
                os.remove(init_file_path)
