from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, null=True, blank=True, 
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.name