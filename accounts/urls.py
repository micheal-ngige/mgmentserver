from django.urls import path
from .views import (
    UserListView, UserDetailView, CurrentUserView,
    DepartmentListView, DepartmentDetailView,
    TeamListView, TeamDetailView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]