from datetime import date, timedelta
from urllib.error import HTTPError

import pandas as pd
from sibdev_project.api.repositories.currency_repository import CurrencyRepository
from sibdev_project.api.services.tracked_currency_service import TrackedCurrencyService
from sibdev_project.api.mail_distribution.mailing import send_email


class CurrencyService:
    def __init__(self):
        self.currency_repository = CurrencyRepository()
        self.tracked_currency_service = TrackedCurrencyService()
        self.daily_file = 'https://www.cbr-xml-daily.ru/daily_json.js'
        self.send_email = send_email

    """
    Проверка существующей даты.
    """

    def check_exist_date(self, checked_date: date):
        return self.currency_repository.check_exist_date(checked_date=checked_date)

    """
    Ежедневное добавление объектов и рассылка писем.
    """

    def daily_add_currencies(self):
        file = self.daily_file
        df = pd.DataFrame(pd.read_json(path_or_buf=file))
        current_date = pd.to_datetime(df['Timestamp'][0].tz_localize(None)).date()
        check = self.check_exist_date(current_date)

        if check is False:
            for index, value in df.iterrows():
                file_datetime = pd.to_datetime(value['Timestamp'].tz_localize(None))
                id = value['Valute']['ID']
                char_code = value['Valute']['CharCode']
                value = float(value['Valute']['Value'])
                self.currency_repository.daily_add_currencies(id=id, datetime_data=file_datetime,
                                                              char_code=char_code, value=value)
            data = self.tracked_currency_service.email_list_to_dict()
            emailing = self.send_email
            for item in data.items():
                email = item[0]
                message = item[1]
                emailing(email=email, message=message)

    """
    Вспомогательная функция для итерации диапазона дат.
    """

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    """
    Добавление архивных данных за указанный период.
    """

    def add_archive_currencies(self):
        end_date = date.today() + timedelta(1)
        start_date = end_date - timedelta(30)

        for single_date in self.daterange(start_date, end_date):
            check = self.check_exist_date(single_date)
            if check is False:
                try:
                    year = single_date.strftime("%Y")
                    month = single_date.strftime("%m")
                    day = single_date.strftime("%d")
                    file = f'https://www.cbr-xml-daily.ru/archive/{year}/{month}/{day}/daily_json.js'
                    print(file)
                    df = pd.DataFrame(pd.read_json(path_or_buf=file))
                    print(single_date)

                    for index, value in df.iterrows():
                        id = value['Valute']['ID']
                        file_date = pd.to_datetime(value['Timestamp'].tz_localize(None))
                        char_code = value['Valute']['CharCode']
                        value = float(value['Valute']['Value'])
                        self.currency_repository.daily_add_currencies(id=id, datetime_data=file_date,
                                                                      char_code=char_code,
                                                                      value=value)
                except HTTPError:
                    pass

    """
    Возвращение списка объектов с учетом указанной сортировки.
    """

    def get_rates(self, parameter: None | str = None):
        if parameter == 'value':
            return self.currency_repository.get_asc_rates()
        if parameter == '-value':
            return self.currency_repository.get_desc_rates()
        return self.currency_repository.get_rates()

    """
    Возвращение ответа превышено ли пороговое значение пользователя.
    """

    def is_threshold_exceeded(self, currency_id: int, start_date: date, end_date: date):
        return self.currency_repository.is_threshold_exceeded(currency_id=currency_id, start_date=start_date,
                                                              end_date=end_date)
