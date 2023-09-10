from django.core.management.base import BaseCommand
from sibdev_project.api.services.currency_service import CurrencyService

"""
Команда для загрузки архивных данных.
"""


class Command(BaseCommand):
    help = 'Сommand to download the archive for the last 30 days'

    def handle(self, *args, **kwargs):
        CurrencyService().add_archive_currencies()
        self.stdout.write('Archive downloaded.')
