"""
django command for wait for db
"""
import time
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OError
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('waiting for db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OError, OperationalError):
                self.stdout.write('database is unavailable waiting 1s...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('db is available now!'))
