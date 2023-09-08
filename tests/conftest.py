from pytest_factoryboy import register
from rest_framework.test import APIClient
import pytest
from .factories import CategoryFactory, BrandFactory, ProductFactory, ProductLineFactory

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)

@pytest.fixture
def api_client():
    return APIClient