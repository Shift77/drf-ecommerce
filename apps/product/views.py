from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from django.db.models import Prefetch


class CategoryViewSet(viewsets.ViewSet):

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    
    queryset = Product.objects.actives_only() # Calling a custom query set function created in .models.py
    
    lookup_field = 'slug'
    
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)  
    
    @extend_schema(responses=ProductSerializer)
    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related('category', 'brand')
            .prefetch_related(Prefetch('product_line__product_image'))
            ,many=True)
        return Response(serializer.data)
    
    @action(
        detail=False,
        methods=['GET'],
        url_path=r'category/(?P<category_name>\w+)/all',
        url_name='all', 
    )
    @extend_schema(responses=ProductSerializer)
    def list_by_category_name(self, request, category_name=None):
        serializer = ProductSerializer(self.queryset.filter(category__name=category_name), 
                                       many=True)
        return Response(serializer.data)
        
        