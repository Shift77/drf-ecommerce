from django.contrib import admin
from .models import Category, Brand, Product, ProductLine
# Register your models here.

class ProductLineInline(admin.TabularInline):
    model = ProductLine
@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductLineInline]

admin.site.register(Category)
admin.site.register(Brand)
