from django.contrib import admin
from .models import (
    Category, 
    Brand, 
    Product, 
    Attribute, 
    ProductLine, 
    ProductImage, 
    AttributeValue,
    ProductType
    )

from django.urls import reverse
from django.utils.safestring import mark_safe





class HyperLinkInline(object):
    
    def edit(self, instance):
        
        url = reverse(
            f'admin:{instance._meta.app_label}_{instance._meta.model_name}_change',
            args=[instance.pk,]
        )
        
        if instance.pk:
            link = mark_safe(f'<a href={url}>edit</a>')
            return link
        else:
            return ''
        

class ProductLineInline(HyperLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ('edit',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    
    
class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.product_line.through # referencing the ManyToMany related name
                                                # for AttributeValue in ProductLine

class AttributeInline(admin.TabularInline):
    model = Attribute.product_type.through

@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductLineInline,]

@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueInline]

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = (AttributeInline,)


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
# admin.site.register(ProductType)
