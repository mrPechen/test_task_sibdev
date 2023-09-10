from rest_framework import serializers
from sibdev_project.api.models import Currency

"""
Сериалайзер для вывода списка объектов.
"""


class RatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "charcode", "datetime", "value"]


"""
Сериалайзер с дополнительными полями для аналитики данных.
"""


class AdditionalFieldsSerializer(serializers.ModelSerializer):
    is_threshold_exceeded = serializers.SerializerMethodField()
    threshold_match_type = serializers.SerializerMethodField()
    is_min_value = serializers.SerializerMethodField()
    is_max_value = serializers.SerializerMethodField()
    percentage_ratio = serializers.SerializerMethodField()

    def get_is_threshold_exceeded(self, obj):
        value = obj.value
        threshold = float(self.context['threshold'])
        if value > threshold:
            return True
        return False

    def get_threshold_match_type(self, obj):
        value = obj.value
        threshold = float(self.context['threshold'])
        if value > threshold:
            return 'less'
        if value < threshold:
            return 'exceeded'
        elif value == threshold:
            return 'equal'

    def get_is_min_value(self, obj):
        value = obj.value
        min_value = self.context['min_value']
        if value in min_value:
            return True
        else:
            return False

    def get_is_max_value(self, obj):
        value = obj.value
        max_value = self.context['max_value']
        if value in max_value:
            return True
        else:
            return False

    def get_percentage_ratio(self, obj):
        value = obj.value
        threshold = float(self.context['threshold'])
        result = value / threshold * 100
        return float(format(result, '.2f'))


"""
Сериалайзер для вывода объектов для аналитики с дополнительными полями.
"""


class AnalyticsObjectSerializer(AdditionalFieldsSerializer):
    class Meta:
        model = Currency
        fields = ["id", "charcode", "datetime", "value", 'is_threshold_exceeded',
                  'threshold_match_type', 'is_min_value', 'is_max_value', 'percentage_ratio']
