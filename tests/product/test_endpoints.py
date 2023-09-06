
import pytest
import json 

pytestmark = pytest.mark.django_db

class TestCategoryEndpoints:
    
    endpoint = '/api/category/'
    
    def test_category_get(self, category_factory, api_client):
        
        category_factory.create_batch(10)
        
        response = api_client().get(self.endpoint)
        
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10
        
class TestBrandEndpoint:
    
    endpoint = '/api/brand/'
    
    def test_brand_get(self, brand_factory, api_client):
        
        brand_factory()
        
        response = api_client().get(self.endpoint)
        
        assert response.status_code == 200
        

class TestProductEndpoint:
    
    endpoint = '/api/product/'
    
    def test_product_get(self, product_factory, api_client):
        
        product_factory
        
        response = api_client().get(self.endpoint)
        
        assert response.status_code == 200