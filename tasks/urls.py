from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView,
    TaskListView, TaskDetailView,
    TaskCommentListView, TaskCommentDetailView,
    TaskDelegationListView, TaskDelegationDetailView, ApproveDelegationView
)

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    
    path('task-comments/', TaskCommentListView.as_view(), name='task-comment-list'),
    path('task-comments/<int:pk>/', TaskCommentDetailView.as_view(), name='task-comment-detail'),
    
    path('task-delegations/', TaskDelegationListView.as_view(), name='task-delegation-list'),
    path('task-delegations/<int:pk>/', TaskDelegationDetailView.as_view(), name='task-delegation-detail'),
    path('task-delegations/<int:pk>/approve/', ApproveDelegationView.as_view(), name='approve-delegation'),
]