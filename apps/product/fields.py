from typing import Any
from django.core.checks import CheckMessage
from django.db import models
from django.core import checks
from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    
    description = 'A custom field to order'
    
    def __init__(self, unique_field=None ,*args: Any, **kwargs: Any):
        self.unique_field = unique_field
        super().__init__(*args, **kwargs)
        
    def check(self, **kwargs):
        return [
            *super().check(**kwargs), 
            *self._check_unique_field(),
        ]
    
    def _check_unique_field(self):
        if self.unique_field is None:
            return [checks.Error('unique_field must be filled')]
        
        elif self.unique_field not in (f.name for f in self.model._meta.get_fields()):
            return [checks.Error('unique field does not match any existing field!')]
        
        return []
        
    def pre_save(self, model_instance: Model, add: bool) -> Any:
        
        if getattr(model_instance, self.attname) is None:
            
            queryset = self.model.objects.all()
            
            try:
                q = {
                    self.unique_field: getattr(model_instance, self.unique_field)
                }
                
                queryset = queryset.filter(**q)
                last_item = queryset.latest(self.attname)
                value = last_item.order + 1
                
            except ObjectDoesNotExist:
                value = 1
        
            return value  
        else:      
            return super().pre_save(model_instance, add)
    