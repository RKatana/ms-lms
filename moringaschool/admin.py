from django.contrib import admin
from .models import (
    Cohort, Course, Module, Content, File, Image, Video, Text
)

model_list = [Cohort, Course, Module, Content, File, Image, Video, Text]    
[admin.site.register(model) for model in model_list] #registering models in the admin using a list comprehension
