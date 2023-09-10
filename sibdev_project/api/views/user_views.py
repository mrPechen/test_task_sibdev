from typing import Any

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sibdev_project.api.serializers.user_serializers import UserSerializer

"""
Обработка запроса на создание нового пользователя.
"""


@api_view(['POST'])
def registration_new_user(request: Any):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)
