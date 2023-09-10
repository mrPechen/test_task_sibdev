from typing import Any

from sibdev_project.api.models import User


class UserRepository:
    def __init__(self):
        self.user_model = User

    """
    Запрос в БД для создания нового пользователя.
    """

    def create_user(self, email: str, password: Any):
        user = self.user_model.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user
