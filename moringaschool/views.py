from django.shortcuts import render
from typing import Any, TypeVar as T, QuerySet
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (
                                        CreateView,
                                        UpdateView,
                                        DeleteView
                                    )
from django.contrib.auth.mixins import (
                                        LoginRequiredMixin,
                                        PermissionRequiredMixin
                                    )
from moringaschool.models import Course

class OwnerMixin(object):
    '''Owner mixin class'''
    def get_queryset(self) -> QuerySet[T]:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    '''This mixin class implements the form_valid method. It is executed whenever a form is submitted.
       This sets the current user as the owner
    '''
    def form_valid(self, form) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    '''This is the view for course management.
       The class overrides the get_queryset method of ListView to only retrieve courses created by the current user
    '''
    model = Course
    template_name = '/courses/manage/list.html'
    permission_required = 'courses.view_course'

    def get_queryset(self) -> QuerySet[T]:
        qs = super().get_queryset()
        return qs.filter(owner= self.request.user)

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/delete.html'
    permission_required = 'courses.delete_course'