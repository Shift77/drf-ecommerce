import pytest
from django.core.exceptions import ValidationError
pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        
        # Act
        obj = category_factory(name='cat_test')
        # Assert
        assert obj.__str__() == 'cat_test'


class TestBrandModel:
    def test_str_method_brand(self, brand_factory):
        
        obj = brand_factory(name='brand_test')
        
        assert obj.__str__() == 'brand_test'


class TestProductModel:
    def test_str_method_product(self, product_factory):
        
        obj = product_factory(name='product_test')
        
        assert obj.__str__() == 'product_test'
        
class TestProductLineModel:
    
    def test_clean_method(self, product_line_factory, product_factory):
        prod = product_factory()
        obj_1 = product_line_factory(order=1, product=prod)
        
        with pytest.raises(ValidationError):
            obj_2 = product_line_factory(order=1, product=prod)
            obj_2.clean()
        
    def test_str_method(self, product_line_factory):
        
        obj = product_line_factory(sku='555')
        
        assert obj.__str__() == '555'