from django.core.management.base import BaseCommand
from myapp.models import Employee
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the Employee table with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            position = fake.job()
            office = fake.city()
            start_date = fake.date_between(start_date='-10y', end_date='today')
            salary = round(random.uniform(30000, 150000), 2)

            Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                position=position,
                office=office,
                start_date=start_date,
                salary=salary
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the Employee table'))
