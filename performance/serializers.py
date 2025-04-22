from rest_framework import serializers
from .models import PerformanceReview, KPI, UserKPI

class PerformanceReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = PerformanceReview
        fields = '__all__'

class KPISerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = KPI
        fields = '__all__'

class UserKPISerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    kpi_name = serializers.CharField(source='kpi.name', read_only=True)
    
    class Meta:
        model = UserKPI
        fields = '__all__'