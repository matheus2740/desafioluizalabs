from django.core.management.base import BaseCommand

from employee_manager.fixture_util import create_departments, create_employees, create_admin, associate_heads


class Command(BaseCommand):
    help = 'Create fake data and insert it into the database.'

    def handle(self, *args, **options):

        create_departments(10)
        create_employees(100)
        create_admin()
        associate_heads()
