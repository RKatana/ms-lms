from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django_resized import ResizedImageField
from django.template.loader import render_to_string

class Cohort(models.Model):
    title    = models.CharField(max_length=240)
    slug     = models.SlugField(max_length=240, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title',)

class Course(models.Model):
    owner    = models.ForeignKey(User, related_name= 'courses_created', on_delete=models.CASCADE)
    cohort   = models.ForeignKey(Cohort, related_name='courses', on_delete=models.CASCADE) 
    title    = models.CharField(max_length=240)
    slug     = models.SlugField(max_length=240, unique=True)
    overview = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(User, related_name='courses_joined', blank = True)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-created']

class Module(models.Model):
    course  = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title   = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    
    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']

class Content(models.Model):
    module = models.ForeignKey(Module, related_name= 'contents', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, 
                                    on_delete=models.CASCADE,
                                    limit_choices_to={
                                        'model__in':(
                                            'text',
                                            'video',
                                            'image',
                                            'file'
                                        )
                                    })
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    '''An abstract model for different content items defined below'''
    owner   = models.ForeignKey(User, related_name="%(class)s_related", on_delete=models.CASCADE)
    title   = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
        
    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html',{'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = ResizedImageField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()