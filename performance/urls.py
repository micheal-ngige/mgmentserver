from django.urls import path
from .views import (
    PerformanceReviewListView, PerformanceReviewDetailView, ApprovePerformanceReviewView,
    KPIListView, KPIDetailView,
    UserKPIListView, UserKPIDetailView
)

urlpatterns = [
    path('reviews/', PerformanceReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', PerformanceReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:pk>/approve/', ApprovePerformanceReviewView.as_view(), name='approve-review'),
    
    path('kpis/', KPIListView.as_view(), name='kpi-list'),
    path('kpis/<int:pk>/', KPIDetailView.as_view(), name='kpi-detail'),
    
    path('user-kpis/', UserKPIListView.as_view(), name='user-kpi-list'),
    path('user-kpis/<int:pk>/', UserKPIDetailView.as_view(), name='user-kpi-detail'),
]