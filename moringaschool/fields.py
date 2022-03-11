from dataclasses import field
from typing import Any
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    '''A subclass of PositiveIntegerField that creates a custom order for items added to the database
        Args: for_field - an optional param that allows you to indicate the fields the order \
             has to be calculated with respect to.'''
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance: models.Model, add: bool) -> Any:
        """This method overwrites the PositveIntegerField `pre_save` \ 
            which executes before saving the field into the database"""
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) \
                            for field in self.for_fields}
                    qs = qs.filter(**query)
                last_elm = qs.latest(self.attname)
                value = last_elm.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
