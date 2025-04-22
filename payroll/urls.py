from django.urls import path
from .views import (
    PayrollListView, PayrollDetailView,
    PayslipListView, PayslipDetailView, GeneratePayslipView,
    TaxConfigurationListView, TaxConfigurationDetailView
)

urlpatterns = [
    path('payrolls/', PayrollListView.as_view(), name='payroll-list'),
    path('payrolls/<int:pk>/', PayrollDetailView.as_view(), name='payroll-detail'),
    
    path('payslips/', PayslipListView.as_view(), name='payslip-list'),
    path('payslips/<int:pk>/', PayslipDetailView.as_view(), name='payslip-detail'),
    path('payslips/generate/', GeneratePayslipView.as_view(), name='generate-payslip'),
    
    path('tax-configs/', TaxConfigurationListView.as_view(), name='tax-config-list'),
    path('tax-configs/<int:pk>/', TaxConfigurationDetailView.as_view(), name='tax-config-detail'),
]