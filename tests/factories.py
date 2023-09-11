import factory

from apps.product.models import (
    Category, 
    Brand, 
    Product, 
    ProductLine, 
    ProductImage, 
    ProductType,
    Attribute,
    AttributeValue
    )


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute
    name = 'test'
        

class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute
    name = 'test'

        
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        
    name='test'

class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        
    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or  not extracted:
            return
        self.attribute.add(*extracted)

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
       model = Brand
       
    name='test'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product 
        
    name = 'test'
    product_type = factory.SubFactory(ProductTypeFactory)
    
    

class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        
    price = 120.00
    sku = '555'
    stock_qty = 5
    product = factory.SubFactory(ProductFactory)
    
    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or  not extracted:
            return
        self.attribute_value.add(*extracted)
    
    
class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage
        
    url = 'test_url'
    alternative_text = 'alt_text'
    product_line = factory.SubFactory(ProductLineFactory)
    order = 1

