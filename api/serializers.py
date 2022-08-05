from rest_framework import serializers

from api.models import CreditCard, Payment, Order

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = [
            "id",
            "last_4",
            "brand",
            "exp_month",
            "exp_year",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_total",
            "status",
            "success_date",
            # "ebt_total",
        ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order", # The id of the associated Order object
            "amount",
            "description",
            "payment_method", # The id of the associated CreditCard object
            "status",
            "success_date",
            "last_processing_error"
        ]
