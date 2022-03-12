from django.urls import path
from .views import (
                    ManageCourseListView,
                    CourseCreateView,
                    CourseUpdateView,
                    CourseDeleteView,
                    CourseModuleUpdateView,
                    ContentCreateUpdateView,
                    ContentDeleteView,
                    ModuleContentListView,
                    ModuleOrderView, 
                    ContentOrderView,
                )


urlpatterns =[
    path('course-list/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name= 'course_update' ),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/module', CourseModuleUpdateView.as_view(), name= 'course_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/', ContentCreateUpdateView.as_view(),name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',ContentCreateUpdateView.as_view(),name='module_content_update'),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(),name='module_content_delete'),
    path('module/<int:module_id>/', ModuleContentListView.as_view(), name='module_content_list'),
    path('module/order/', ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', ContentOrderView.as_view(), name='content_order'),
]