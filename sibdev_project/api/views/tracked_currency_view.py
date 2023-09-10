from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sibdev_project.api.serializers.tracked_currency_serializer import AddTrackedSerializer

"""
Обработка запроса на добавление отслеживаемых объектов.
"""


@api_view(['POST'])
def add_tracked_currency(request):
    serializer = AddTrackedSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.user.email
    serializer.save(email=email)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
