from django.urls import path
from .views import (
                    ManageCourseListView,
                    CourseCreateView,
                    CourseUpdateView,
                    CourseDeleteView
                )


urlpatterns =[
    path('course-list/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name= 'course_update' ),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete')
]