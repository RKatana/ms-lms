from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django_registration.forms import RegistrationForm
from django_registration.views import RegistrationView
from django_registration import signals
from .forms import CourseEnrollForm
from moringaschool.models import Course
from django.template.loader import render_to_string
from django.core import signing
from django.contrib.sites.shortcuts import get_current_site

REGISTRATION_SALT = getattr(settings, "REGISTRATION_SALT", "registration")

class StudentRegistrationView(RegistrationView):
    email_body_template = "django_registration/activation_email_body.txt"
    email_subject_template = "django_registration/activation_email_subject.txt"
    success_url = reverse_lazy("django_registration_complete")

    def register(self, form):
        new_user = self.create_inactive_user(form)
        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=self.request
        )
        return new_user

    

    def get_activation_key(self, user):
        """
        Generate the activation key which will be emailed to the user.

        """
        return signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)

    def get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.

        """
        scheme = "https" if self.request.is_secure() else "http"
        return {
            "scheme": scheme,
            "activation_key": activation_key,
            "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
            "site": get_current_site(self.request),
        }

    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save(commit=False)
        new_user.first_name = 'TM'
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user
    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request,
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = "".join(subject.splitlines())
        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request,
        )
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    # template_name = 'students/course/enroll.html'
    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.student.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(student__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(student__in=[self.request.user])
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            try:    
                context['module'] = course.modules.all()[0]
            except IndexError:
                context = None
        return context