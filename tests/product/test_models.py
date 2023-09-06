import pytest

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