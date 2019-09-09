from rest_framework import serializers


class AutoTradeOnOffSerializer(serializers.Serializer):
    auto_trade_is_on = serializers.BooleanField

    # def create(self, validated_data):
    #     return Comment(**validated_data)

    def update(self, validated_data):

        return validated_data
