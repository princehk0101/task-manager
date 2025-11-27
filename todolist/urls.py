from django.urls import path,include
from . import views
from .views import contact_view
from rest_framework import routers
from .views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('todolist/', views.todolist, name='todolist'),
    path('delete_task/<task_id>', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('pending/<int:task_id>/', views.pending_task, name='pending_task'),

    path('about/', views.about, name='about'),
    path('contact/', contact_view, name='contact'),

    path('', include(router.urls)),
]
