"""ms_lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

from moringaschool.views import CourseListView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(next_page=reverse_lazy('manage_course_list')), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page= reverse_lazy('login')), name='logout'),
    path('students/', include('students.urls')),
    path('admin/', admin.site.urls),
    path('course/', include('moringaschool.urls')),
    path('', CourseListView.as_view(), name='course_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
