from rest_framework import serializers
from django.utils import timezone
from .models import Invoice, InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    """This is the invoice detail serializer"""
    def validate_positive_decimal(self, value, field_name):
        """
        Validate a field to ensure that it is a positive decimal number.
        """
        if value <= 0:
            raise serializers.ValidationError(f"{field_name.capitalize()} must be a positive decimal number")
        return value

    def validate_unit_price(self, value):
        return self.validate_positive_decimal(value, "unit_price")
    
    class Meta:
        model = InvoiceDetail
        fields = [
            'id',
            'description',
            'quantity',
            'unit_price',
            'price',
        ]
        extra_kwargs = {
            'price': {'read_only': True}
        }


class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True, required=False)
 
    def validate_date(self, value):
        """ Validate the 'date' field to ensure that it is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future")
        return value
    
    def validate_customer_name(self, value):
        """ Validate the 'customer_name' field to ensure that it is at least 3 characters long"""
        if len(value) < 3:
            raise serializers.ValidationError("Customer name must be at least 3 characters long")
        return value

    class Meta:
        model = Invoice
        fields = [
            'id',
            'date',
            'customer_name',
            'details'
        ]

        