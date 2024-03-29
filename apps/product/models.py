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
    
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='product')

    
    objects = ActiveQueryset.as_manager() # appending a new queryset function to object manager 
        
    def __str__(self):
        return self.name
    
    
class Attribute(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
        

class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, 
        on_delete=models.CASCADE, 
        related_name='attribute_value'
        )   
    
    def __str__(self) -> str:
        return f'{self.attribute} : {self.attribute_value}'

class ProductLine(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sku = models.CharField(max_length=255)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_line')
    order = OrderField(unique_field='product', blank=True)
    is_active = models.BooleanField(default=False)
    attribute_value = models.ManyToManyField(
        AttributeValue,     
        through='ProductLineAttributeValue',
        related_name='product_line',
        )    
    
    product_type = models.ForeignKey('ProductType', null=True, blank=True,on_delete=models.PROTECT)

    
    def __str__(self):
        return self.sku
    
    def clean(self):    
        queryset = ProductLine.objects.filter(product=self.product)
        
        for q in queryset:
            if self.id != q.id and self.order == q.order:
                raise ValidationError('Order value is duplicated!')


class ProductLineAttributeValue(models.Model):
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('product_line', 'attribute_value')
    
    
    def clean(self):
        
        query = ProductLineAttributeValue.objects.filter(attribute_value=self.attribute_value).filter(product_line=self.product_line).exists()
        
        if not query:
            q = Attribute.objects.filter(
                attribute_value__product_line=self.product_line
                ).values_list('pk', flat=True)
            if self.attribute_value.attribute.id in q:
                raise ValidationError('Duplicate attribute!')


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to='images/')
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_field='product_line', blank=True)
    
    
    def __str__(self):
        return str(self.url)


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    attribute = models.ManyToManyField(Attribute, through='ProductTypeAttribute', related_name='product_type')
    
    def __str__(self):
        return str(self.name)
    
    
class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT,
                                     related_name='product_type_attribute_p')
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT,
                                  related_name='product_type_attribute_a')
    
    class Meta:
        unique_together = ('product_type', 'attribute')
    

    
    
    
    
    
    
    