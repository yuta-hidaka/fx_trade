from rest_framework import serializers
from ...models import M5_USD_JPY


class SetCandleSerializer(serializers.Serializer):
    record_time = serializers.DateTimeField()
    open = serializers.DecimalField(max_digits=8, decimal_places=4)
    close = serializers.DecimalField(max_digits=8, decimal_places=4)
    high = serializers.DecimalField(max_digits=8, decimal_places=4)
    low = serializers.DecimalField(max_digits=8, decimal_places=4)

    def update(self, validated_data):

        return validated_data

    def create(self, validated_data):

        result, created = M5_USD_JPY.objects.filter(
            record_time=validated_data['record_time']).get_or_create(
            record_time=validated_data['record_time'],
            open=validated_data['open'],
            close=validated_data['close'],
            high=validated_data['high'],
            low=validated_data['low'],
        )

        print(validated_data['record_time'])
        print("created")
        print(created)

        return validated_data
