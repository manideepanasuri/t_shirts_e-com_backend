from rest_framework import serializers
from store.serializers import ProductSerializer,ProductVariationSerializer
from .models import *

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    productVariation=serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'
    def get_product(self, obj):
        return ProductSerializer(obj.productVariation.product).data
    def get_productVariation(self, obj):
        return ProductVariationSerializer(obj.productVariation).data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    productVariation=serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_productVariation(self, obj):
        return  ProductVariationSerializer(obj.product_variation).data


class OrderSerializer(serializers.ModelSerializer):
    orderItems=serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'
    def get_orderItems(self, obj):
        return OrderItemSerializer(obj.order_item,many=True).data
