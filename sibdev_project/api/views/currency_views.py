from sibdev_project.api.services.currency_service import CurrencyService
from sibdev_project.api.serializers.currency_serializers import RatesSerializer, AnalyticsObjectSerializer
from sibdev_project.api.services.tracked_currency_service import TrackedCurrencyService
from typing import Any

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

"""
Обработка запроса на вывод списка объектов для анонимного и авторизованного пользователя.
"""


@api_view(['GET'])
@permission_classes([AllowAny | IsAuthenticated])
def get_rates(request: Any):
    parameter = None
    params = request.query_params
    if params:
        if request.GET['value'] == 'value':
            parameter = 'value'
        if request.GET['value'] == '-value':
            parameter = '-value'
    if request.user.is_authenticated:
        email = request.user.email
        data = TrackedCurrencyService().get_tracked_currency(email=email, parameter=parameter)
        serializer = RatesSerializer(data, many=True)
        return Response(serializer.data)
    data = CurrencyService().get_rates(parameter=parameter)
    serializer = RatesSerializer(data, many=True)
    return Response(serializer.data)


"""
Обработка запроса для вывода объектов для аналитики.
"""


@api_view(['GET'])
def analytics(request, id: int):
    if request.method == 'GET':
        if not request.query_params:
            return Response({"Error": {"detail": "no keys 'date_from', 'date_to', 'threshold' found"}})
        currency_id = id
        start_date = request.GET['date_from']
        end_date = request.GET['date_to']
        threshold = request.GET['threshold']
        data = CurrencyService().is_threshold_exceeded(currency_id=currency_id, start_date=start_date,
                                                       end_date=end_date)
        min_value = [i.min_value for i in data]
        max_value = [i.max_value for i in data]
        serializer = AnalyticsObjectSerializer(data=data, context={"id": id, "start_date": start_date,
                                                                   "end_date": end_date, "threshold": threshold,
                                                                   "min_value": min_value,
                                                                   "max_value": max_value}, many=True)
        serializer.is_valid()
        return Response(serializer.data)
