from sibdev_project.api.models import TrackedCurrency
from sibdev_project.api.models import User
from sibdev_project.api.models import Currency
from django.db.models import F


class TrackedCurrencyRepository:
    def __init__(self):
        self.tracked_currency_model = TrackedCurrency
        self.user_model = User
        self.currency_model = Currency

    """
    Запрос в БД на добавление отслеживаемых объектов.
    """

    def add_tracked_currency(self, email: str, currency_id: int, threshold: float):
        user = self.user_model.objects.get(email=email)
        result = self.tracked_currency_model.objects.create(user=user, currency=currency_id, threshold=threshold)
        result.save()
        return result

    """
    Запрос в БД для вывода отслеживаемых объектов.
    """

    def get_tracked_currency(self, email: str):
        user = self.user_model.objects.get(email=email).id
        last_date = self.currency_model.objects.order_by('datetime').values('datetime').last()
        charcode_list = self.tracked_currency_model.objects.filter(user=user).values_list('currency_id__charcode',
                                                                                          flat=True)
        result = self.currency_model.objects.filter(charcode__in=charcode_list, datetime=last_date['datetime']).all()
        return result

    """
    Запрос в БД для вывода отслеживаемых объектов отсортированных по возрастанию.
    """

    def get_asc_tracked_currency(self, email: str):
        user = self.user_model.objects.get(email=email).id
        last_date = self.currency_model.objects.order_by('datetime').values('datetime').last()
        charcode_list = self.tracked_currency_model.objects.filter(user=user).values_list('currency_id__charcode',
                                                                                          flat=True)
        result = self.currency_model.objects.filter(charcode__in=charcode_list,
                                                    datetime=last_date['datetime']).order_by(
            'value')
        return result

    """
    Запрос в БД для вывода отслеживаемых объектов отсортированных по убыванию.
    """

    def get_desc_tracked_currency(self, email: str):
        user = self.user_model.objects.get(email=email).id
        last_date = self.currency_model.objects.order_by('datetime').values('datetime').last()
        charcode_list = self.tracked_currency_model.objects.filter(user=user).values_list('currency_id__charcode',
                                                                                          flat=True)
        result = self.currency_model.objects.filter(charcode__in=charcode_list,
                                                    datetime=last_date['datetime']).order_by(
            '-value')
        return result

    """
    Запрос в БД для получения списка эмеилов и валют, чьи пороговые значения были превышены.
    """

    def email_list(self):
        last_date = self.currency_model.objects.order_by('datetime').values('datetime').last()
        charcode_list = self.currency_model.objects.filter(datetime=last_date['datetime']).values_list('charcode',
                                                                                                       flat=True)
        result = self.tracked_currency_model.objects.filter(currency_id__charcode__in=charcode_list,
                                                            threshold__lt=F('currency_id__value')).values_list(
            'user_id__email', 'currency_id__charcode')
        return result
