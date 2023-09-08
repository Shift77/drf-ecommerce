from rest_framework import serializers
from .models import Category, Brand, Product, ProductLine, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['product_line', 'id']


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    class Meta:
        model = ProductLine
        exclude = ['product']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    brand_name = serializers.CharField(source='brand.name')
    product_line = ProductLineSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'brand_name',
            'category_name',
            'product_line',
        ]


