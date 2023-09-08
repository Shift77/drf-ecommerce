from collections.abc import Collection
from django.db import models
from django.db.models.query import QuerySet
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError

class ActiveQueryset(models.QuerySet):
    '''
    A Queryset class which adds more functionality to other model managers
    
    '''
    
    def actives_only(self):
        return self.all().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager() # appending a new queryset function to object manager
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager() # appending a new queryset function to object manager
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, null=True, blank=True, 
                              on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    
    objects = ActiveQueryset.as_manager() # appending a new queryset function to object manager 
        
    def __str__(self):
        return self.name
    

class ProductLine(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sku = models.CharField(max_length=255)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_line')
    order = OrderField(unique_field='product', blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.sku
    
    def clean(self):    
        queryset = ProductLine.objects.filter(product=self.product)
        
        for q in queryset:
            if self.id != q.id and self.order == q.order:
                raise ValidationError('Order value is duplicated!')


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to='images/')
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_field='product_line', blank=True)
    
    
    def __str__(self):
        return str(self.url)
    
    
    
    
    
    
    
    
    