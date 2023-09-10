from datetime import date, datetime

from sibdev_project.api.models import Currency
from django.db.models import Min, Max


class CurrencyRepository:
    def __init__(self):
        self.currency_model = Currency

    """
    Запрос к БД на добавление данных из JSON файла.
    """

    def daily_add_currencies(self, id: str, datetime_data: datetime, char_code: str, value: float):
        model = self.currency_model
        return model(ID=id, datetime=datetime_data, charcode=char_code, value=value).save()

    """
    Запрос к БД для проверки существующей даты.
    """

    def check_exist_date(self, checked_date: date):
        model = self.currency_model
        result = model.objects.filter(datetime__date=checked_date).exists()
        return result

    """
    Запрос к БД для вывода последних добавленных объектов.
    """

    def get_rates(self):
        model = self.currency_model
        order_by_date = model.objects.order_by('datetime').values('datetime').last()

        result = model.objects.filter(datetime=order_by_date['datetime'])
        return result

    """
    Запрос к БД для вывода последних добавленных объектов отсортированных в порядке возрастания.
    """

    def get_asc_rates(self):
        model = self.currency_model
        order_by_date = model.objects.order_by('datetime').values('datetime').last()
        result = model.objects.filter(datetime=order_by_date['datetime']).order_by('value')
        return result

    """
    Запрос к БД для вывода последних добавленных объектов отсортированных в порядке убывания.
    """

    def get_desc_rates(self):
        model = self.currency_model
        order_by_date = model.objects.order_by('datetime').values('datetime').last()
        result = model.objects.filter(dateime=order_by_date['datetime']).order_by('-value')
        return result

    """
    Запрос в БД для получения объектов за указанный период и их мин. и макс. значений.
    """

    def is_threshold_exceeded(self, currency_id: int, start_date: date, end_date: date):
        model = self.currency_model
        charcode = model.objects.get(id=currency_id).charcode
        result = model.objects.filter(datetime__date__range=[start_date, end_date], charcode=charcode).order_by(
            'datetime').annotate(
            min_value=Min('value'),
            max_value=Max('value'),
        )
        return result
