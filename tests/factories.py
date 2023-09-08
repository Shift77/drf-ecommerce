import factory

from apps.product.models import Category, Brand, Product, ProductLine, ProductImage


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        
    name='test'

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
       model = Brand
       
    name='test'

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product 
        
    name = 'test'
    
class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        
    price = 120.00
    sku = '555'
    stock_qty = 5
    product = factory.SubFactory(ProductFactory)
    

class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage
        
    url = 'test_url'
    alternative_text = 'alt_text'
    product_line = factory.SubFactory(ProductLineFactory)
    order = 1