from typing import Any

from sibdev_project.api.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    """
    Создание нового пользователя.
    """

    def create_user(self, email: str, password: Any):
        result = self.user_repository.create_user(email=email, password=password)
        return result
