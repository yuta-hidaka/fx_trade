from rest_framework import serializers
from ...models import M5_USD_JPY, specifcCandle


class SetSpecificCandleSerializer(serializers.Serializer):
    recorded_at_utc = serializers.DateTimeField()
    open = serializers.DecimalField(max_digits=8, decimal_places=4)
    close = serializers.DecimalField(max_digits=8, decimal_places=4)
    high = serializers.DecimalField(max_digits=8, decimal_places=4)
    low = serializers.DecimalField(max_digits=8, decimal_places=4)

    def update(self, validated_data):
        return validated_data

    def create(self, validated_data):

        result, created = specifcCandle.objects.filter(
            recorded_at_utc=validated_data['recorded_at_utc']).get_or_create(
            recorded_at_utc=validated_data['recorded_at_utc'],
            open=validated_data['open'],
            close=validated_data['close'],
            high=validated_data['high'],
            low=validated_data['low'],
        )

        return result, created


class SetCandleSerializer(serializers.Serializer):
    recorded_at_utc = serializers.DateTimeField()
    open = serializers.DecimalField(max_digits=8, decimal_places=4)
    close = serializers.DecimalField(max_digits=8, decimal_places=4)
    high = serializers.DecimalField(max_digits=8, decimal_places=4)
    low = serializers.DecimalField(max_digits=8, decimal_places=4)

    def update(self, validated_data):
        return validated_data

    def create(self, validated_data):

        result, created = M5_USD_JPY.objects.filter(
            recorded_at_utc=validated_data['recorded_at_utc']).get_or_create(
            recorded_at_utc=validated_data['recorded_at_utc'],
            open=validated_data['open'],
            close=validated_data['close'],
            high=validated_data['high'],
            low=validated_data['low'],
        )

        return result, created
