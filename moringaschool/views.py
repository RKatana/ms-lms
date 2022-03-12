
from django.forms.models import modelform_factory
from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from typing import Any, TypeVar as T
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import (
                                        CreateView,
                                        UpdateView,
                                        DeleteView
                                    )
from django.contrib.auth.mixins import (
                                        LoginRequiredMixin,
                                        PermissionRequiredMixin
                                    )
from moringaschool.models import (
                                    Course,
                                    Content,
                                    Module,
                                )
from moringaschool.forms import ModuleFormSet

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
    fields = ['cohort', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    '''This is the view for course management.
       The class overrides the get_queryset method of ListView to only retrieve courses created by the current user
    '''
    model = Course
    template_name = 'courses/manage/list.html'
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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """This class handles the formset to add, update and delete modules for a specific course"""
    template_name = 'courses/module/formset.html'
    course = None

    def get_formset(self, data = None):
        return ModuleFormSet(instance = self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id= pk, owner = request.user)

        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = {
            'course': self.course,
            'formset': formset
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data= request.POST)
        context = {
            'course': self.course,
            'formset':formset
        }
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(context)