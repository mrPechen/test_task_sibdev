from sibdev_project.api.repositories.tracked_currency_repository import TrackedCurrencyRepository


class TrackedCurrencyService:
    def __init__(self):
        self.repository = TrackedCurrencyRepository()

    """
    Добавление отслеживаемых объектов.
    """

    def add_tracked_currency(self, email: str, currency_id: int, threshold: float):
        result = self.repository.add_tracked_currency(email=email, currency_id=currency_id, threshold=threshold)
        return result

    """
    Получение отслеживаемых объектов.
    """

    def get_tracked_currency(self, email: str, parameter: None | str = None):
        if parameter == 'value':
            return self.repository.get_asc_tracked_currency(email=email)
        if parameter == '-value':
            return self.repository.get_desc_tracked_currency(email=email)
        return self.repository.get_tracked_currency(email=email)

    """
    Создание словаря из списка с названиями почты и списка валют.
    """

    def email_list_to_dict(self):
        data = self.repository.email_list()
        result = {}

        for i in data:
            if i[0] in result:
                result[i[0]].append(i[1])
            else:
                result[i[0]] = [i[1]]

        return result
