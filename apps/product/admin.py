from django.contrib import admin
from .models import Category, Brand, Product, ProductLine, ProductImage
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

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    

        
@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductLineInline,]
    list_display_links = []

@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,]

admin.site.register(Category)
admin.site.register(Brand)
