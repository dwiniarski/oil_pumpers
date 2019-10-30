from django.core.management.base import BaseCommand
from django.db import connection
from django.core import management


class Command(BaseCommand):
    help = 'Resets application to default'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS opdb;")
            cursor.execute("CREATE DATABASE opdb /*!40100 COLLATE 'utf8_general_ci' */;")
            cursor.execute("USE opdb;")

        management.call_command('clear_migrations')
        management.call_command('makemigrations')
        management.call_command('migrate')
        management.call_command('seed')
