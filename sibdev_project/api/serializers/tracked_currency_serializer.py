from rest_framework import serializers
from sibdev_project.api.models import TrackedCurrency
from sibdev_project.api.services.tracked_currency_service import TrackedCurrencyService

"""
Сериалайзер для обработки POST запроса на добавление облеживаемых объектов.
"""


class AddTrackedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedCurrency
        fields = ["currency", "threshold"]

    def create(self, validated_data):
        currency = validated_data['currency']
        threshold = validated_data['threshold']
        email = validated_data['email']
        result = TrackedCurrencyService().add_tracked_currency(email=email, currency_id=currency,
                                                               threshold=float(threshold))
        return result
