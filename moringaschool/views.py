
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.shortcuts import render, redirect, get_object_or_404
from typing import Any, TypeVar as T
from django.db.models.query import QuerySet
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
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
                                    Cohort,
                                )
from moringaschool.forms import ModuleFormSet
from students.forms import CourseEnrollForm
from django.contrib import messages
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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context

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

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/content/form.html'

    def get_model(self, model_name):
        '''This method returns the actual model name or None if the given name does not exist'''
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='moringaschool', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        context = {
            'form': form,
            'object': self.obj
            }
        return self.render_to_response(context)

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,instance=self.obj,data=request.POST,files=request.FILES)
        context ={
            'form': form,
            'object': self.obj
            }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module,item=obj)
                return redirect('module_content_list', self.module.id)
        return self.render_to_response(context)


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,id=id,module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        messages.error(self.request, f"{content.title} has been deleted")
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/module/content_list.html'
    
    def get(self, request, module_id):
        module = get_object_or_404(Module,id=module_id,course__owner=request.user)

        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id = id, course__owner = request.user)\
                .update(order = order)
        return self.render_json_response({"saved": 'OK'})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Course.objects.filter(id = id, course__owner = request.user)\
                .update(order = order)
        return self.render_json_response({"saved": 'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, cohort=None):
        cohorts = Cohort.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if cohort:
            cohort = get_object_or_404(Cohort, slug=cohort)
            courses = courses.filter(cohort=cohort)
        context = {
            'cohorts': cohorts,
            'cohort': cohort,
            'courses': courses
            }
        return self.render_to_response(context)

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
                                initial={'course':self.object})
        return context
