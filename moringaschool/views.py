from django.shortcuts import render
from typing import TypeVar as T, QuerySet
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView
                                      )

from moringaschool.models import Course

class ManageCourseListView(ListView):
    '''This is the view for course management.
       The class overrides the get_queryset method of ListView to only retrieve courses created by the current user
    '''
    model = Course
    template_name = '/courses/list.html'

    def get_queryset(self) -> QuerySet[T]:
        qs = super().get_queryset()
        return qs.filter(owner= self.request.user)
