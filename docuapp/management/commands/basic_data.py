from django.core.management.base import BaseCommand
from docuapp.models import Condition

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):

        condition1 = Condition.objects.create(name='ASIGNADO')
        condition2 = Condition.objects.create(name='DERIVADO')
        condition3 = Condition.objects.create(name='FINALIZADO')
        condition4 = Condition.objects.create(name='RECIBIDO')

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))
