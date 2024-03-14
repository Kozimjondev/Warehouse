from rest_framework import serializers


class ProductsQuantitySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_qty = serializers.IntegerField()


