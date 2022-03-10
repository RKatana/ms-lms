from django.db import models
from django.contrib.auth.models import User

class Cohort(models.Model):
    title    = models.CharField(max_length=240)
    slug     = models.SlugField(max_length=240, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title',)

class Course(models.Model):
    owner    = models.ForeignKey(User, related_name= 'courses_created', on_delete=models.CASCADE)
    module   = models.ForeignKey(Cohort, related_name='courses', on_delete=models.CASCADE) 
    title    = models.CharField(max_length=240)
    slug     = models.SlugField(max_length=240, unique=True)
    overview = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-created']

class Module(models.Model):
    course  = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title   = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

