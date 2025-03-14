import random

from attr import attributes
from rest_framework import serializers

from store.models import Product, Category, ProductVariation, VariationImage, Attribute, AttributeValue, Review, \
    Wishlist


class ProductSerializer(serializers.ModelSerializer):
    ratingsAverage = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
    def get_ratingsAverage(self, obj):
        product_reviews=obj.reviews.all()
        avg=0

        for reivew in product_reviews:
            avg= avg+reivew.rating
        if len(product_reviews)>0:
            avg = avg/len(product_reviews)
        if avg==0:
            avg=4.8
        return avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductVariationSerializer(serializers.ModelSerializer):
    images=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    description=serializers.SerializerMethodField()
    ratingsAverage=serializers.SerializerMethodField()
    price=serializers.SerializerMethodField()
    class Meta:
        model = ProductVariation
        fields = '__all__'
    def get_images(self, obj):
        img=VariationImageSerializer(obj.images.all(), many=True).data
        return img
    def get_name(self, obj):
        return obj.product.name
    def get_description(self, obj):
        return obj.product.description
    def get_ratingsAverage(self, obj):
        product_reviews=obj.product.reviews.all()
        avg=0
        for reivew in product_reviews:
            avg= avg+reivew.rating
        if len(product_reviews)>0:
            avg = avg/len(product_reviews)
        if avg==0:
            avg=4.8
        return avg
    def get_price(self, obj):
        if obj.price is None:
            return obj.product.price
        return obj.price

class VariationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationImage
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
class AttributeValueSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source="attribute.name",read_only=True)
    class Meta:
        model = AttributeValue
        fields = ('attribute', 'value','name')

class ReviewSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = '__all__'
    def get_name(self, obj):
        return obj.user.name

class WishlistSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    price=serializers.SerializerMethodField()
    class Meta:
        model = Wishlist
        fields = '__all__'
    def get_image(self, obj):
        return obj.product.image.url
    def get_name(self, obj):
        return obj.product.name
    def get_price(self, obj):
        return obj.product.price
