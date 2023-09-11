from rest_framework import serializers
from .models import Category, Brand, Product, ProductLine, ProductImage, AttributeValue, Attribute, ProductType


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


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_id = serializers.CharField(source='attribute.id')
    value = serializers.CharField(source='attribute_value')
    class Meta:
        model = AttributeValue
        fields = [
            'attribute_id',
            'value'
        ]

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['name']
        
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Attribute
        
        fields = ['name', 'id']
    
    
         
class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)
    class Meta:
        model = ProductLine
        exclude = ['product']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        at_value = data.pop('attribute_value')
        attr_values = {}
        
        for key in at_value:
            attr_values.update({key['attribute_id']: key['value']})
        
        data.update({'specifications': attr_values})
        return data    
    
    

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    brand_name = serializers.CharField(source='brand.name')
    product_line = ProductLineSerializer(many=True)
    product_type = serializers.SerializerMethodField()

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
            'product_type',
        ]

    def get_product_type(self, obj):
        query = Attribute.objects.filter(product_type__product__id=obj.id)
        return AttributeSerializer(query, many=True).data


    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        at_value = data.pop('product_type')
        attr_values = {}
        
        for key in at_value:
            attr_values.update({key['id']: key['name']})
        
        data.update({'type_specifications': attr_values})
        return data  
    
    
    
    
    