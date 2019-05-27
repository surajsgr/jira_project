from django.urls import path
from .views import TaskCreateView,TaskDetailView,TaskUpdateView,TaskDeleteView,TaskListView
from . import views

urlpatterns = [
    path('', TaskListView.as_view(), name='task-home'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('about/', views.about, name='task-about'),
]