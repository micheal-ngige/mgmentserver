from rest_framework import serializers
from .models import Payroll, Payslip, TaxConfiguration

class PayrollSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Payroll
        fields = '__all__'

class PayslipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Payslip
        fields = '__all__'

class TaxConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxConfiguration
        fields = '__all__'