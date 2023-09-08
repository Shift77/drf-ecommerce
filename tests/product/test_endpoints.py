
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
        
        product_factory()
        
        response = api_client().get(self.endpoint)
        
        assert response.status_code == 200
        
    def test_product_get_slug(self, product_factory, api_client):
        
        slug = 'test-slug'
        endpoint = self.endpoint + '{slug}/'
        product_factory(slug=slug)
        response = api_client().get(endpoint)

        assert response.status_code == 200
        
    def test_product_get_by_category(self, product_factory, api_client, category_factory):
        
        cat = category_factory(name='cat')
        
        prod_1 = product_factory(category=cat)
        prod_2 = product_factory(category=cat)
        
        response = api_client().get(f'{self.endpoint}category/cat/all/')
        
        assert response.status_code == 200
        