from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product


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
    
    queryset = Product.objects.all()
    
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data) 