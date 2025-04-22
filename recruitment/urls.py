from django.urls import path
from .views import (
    JobPositionListView, JobPositionDetailView,
    ApplicantListView, ApplicantDetailView, UpdateApplicantStatusView,
    InterviewListView, InterviewDetailView,
    OnboardingListView, OnboardingDetailView, UpdateOnboardingStatusView
)

urlpatterns = [
    path('positions/', JobPositionListView.as_view(), name='position-list'),
    path('positions/<int:pk>/', JobPositionDetailView.as_view(), name='position-detail'),
    
    path('applicants/', ApplicantListView.as_view(), name='applicant-list'),
    path('applicants/<int:pk>/', ApplicantDetailView.as_view(), name='applicant-detail'),
    path('applicants/<int:pk>/update-status/', UpdateApplicantStatusView.as_view(), name='update-applicant-status'),
    
    path('interviews/', InterviewListView.as_view(), name='interview-list'),
    path('interviews/<int:pk>/', InterviewDetailView.as_view(), name='interview-detail'),
    
    path('onboarding/', OnboardingListView.as_view(), name='onboarding-list'),
    path('onboarding/<int:pk>/', OnboardingDetailView.as_view(), name='onboarding-detail'),
    path('onboarding/<int:pk>/update-status/', UpdateOnboardingStatusView.as_view(), name='update-onboarding-status'),
]