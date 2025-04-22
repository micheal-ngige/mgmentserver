from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Payroll, Payslip, TaxConfiguration
from .serializers import PayrollSerializer, PayslipSerializer, TaxConfigurationSerializer
from accounts.models import User
from django.db.models import Q

class PayrollListView(generics.ListCreateAPIView):
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return Payroll.objects.all()
        elif user.role == 'MANAGER':
            # Get payroll for users in the manager's department
            return Payroll.objects.filter(user__department=user.department)
        else:
            return Payroll.objects.filter(user=user)

class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class PayslipListView(generics.ListAPIView):
    serializer_class = PayslipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return Payslip.objects.all()
        elif user.role == 'MANAGER':
            # Get payslips for users in the manager's department
            return Payslip.objects.filter(user__department=user.department)
        else:
            return Payslip.objects.filter(user=user)

class PayslipDetailView(generics.RetrieveAPIView):
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class GeneratePayslipView(generics.CreateAPIView):
    serializer_class = PayslipSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        month = request.data.get('month')
        year = request.data.get('year')
        
        if not all([user_id, month, year]):
            return Response({'detail': 'user_id, month, and year are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if payslip already exists for this user/month/year
        if Payslip.objects.filter(user=user, month=month, year=year).exists():
            return Response({'detail': 'Payslip already exists for this period.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate payroll components
        basic_salary = Payroll.objects.filter(
            user=user, 
            type='SALARY', 
            is_active=True
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        allowances = Payroll.objects.filter(
            user=user, 
            type='ALLOWANCE', 
            is_active=True
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        deductions = Payroll.objects.filter(
            user=user, 
            type='DEDUCTION', 
            is_active=True
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        bonuses = Payroll.objects.filter(
            user=user, 
            type='BONUS', 
            is_active=True,
            effective_date__month=month,
            effective_date__year=year
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        # Calculate tax (simplified)
        taxable_income = basic_salary + allowances + bonuses - deductions
        tax_config = TaxConfiguration.objects.filter(
            min_amount__lte=taxable_income,
            max_amount__gte=taxable_income,
            is_active=True
        ).first()
        
        tax = 0
        if tax_config:
            tax = taxable_income * (tax_config.tax_percentage / 100)
        
        net_salary = taxable_income - tax
        
        
        payslip_data = {
            'user': user.id,
            'month': month,
            'year': year,
            'basic_salary': basic_salary,
            'allowances': allowances,
            'deductions': deductions,
            'bonuses': bonuses,
            'tax': tax,
            'net_salary': net_salary,
        }
        
        serializer = self.get_serializer(data=payslip_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaxConfigurationListView(generics.ListCreateAPIView):
    queryset = TaxConfiguration.objects.all()
    serializer_class = TaxConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class TaxConfigurationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaxConfiguration.objects.all()
    serializer_class = TaxConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]