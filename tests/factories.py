import factory

from apps.product.models import Category, Brand, Product


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