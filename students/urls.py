from django.urls import path, include
from .views import (StudentRegistrationView,
                    StudentEnrollCourseView,
                    StudentCourseListView,
                    StudentCourseDetailView,

                    )

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name = 'student_registration'),
    # path('register', include('django_registration.backends.activation.urls')),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/',StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<pk>/<module_id>/',StudentCourseDetailView.as_view(), name='student_course_detail_module'),
]