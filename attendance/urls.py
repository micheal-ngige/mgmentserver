from django.urls import path
from .views import (
    ShiftListView, ShiftDetailView,
    AttendanceListView, AttendanceDetailView, CheckInView, CheckOutView,
    LeaveTypeListView, LeaveTypeDetailView,
    LeaveRequestListView, LeaveRequestDetailView, ApproveLeaveView, RejectLeaveView
)

urlpatterns = [
    path('shifts/', ShiftListView.as_view(), name='shift-list'),
    path('shifts/<int:pk>/', ShiftDetailView.as_view(), name='shift-detail'),
    
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),
    path('attendance/check-in/', CheckInView.as_view(), name='check-in'),
    path('attendance/check-out/', CheckOutView.as_view(), name='check-out'),
    
    path('leave-types/', LeaveTypeListView.as_view(), name='leave-type-list'),
    path('leave-types/<int:pk>/', LeaveTypeDetailView.as_view(), name='leave-type-detail'),
    
    path('leave-requests/', LeaveRequestListView.as_view(), name='leave-request-list'),
    path('leave-requests/<int:pk>/', LeaveRequestDetailView.as_view(), name='leave-request-detail'),
    path('leave-requests/<int:pk>/approve/', ApproveLeaveView.as_view(), name='approve-leave'),
    path('leave-requests/<int:pk>/reject/', RejectLeaveView.as_view(), name='reject-leave'),
]