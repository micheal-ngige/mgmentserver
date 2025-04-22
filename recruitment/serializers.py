from rest_framework import serializers
from .models import JobPosition, Applicant, Interview, Onboarding

class JobPositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = JobPosition
        fields = '__all__'

class ApplicantSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(source='position.title', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Applicant
        fields = '__all__'

class InterviewSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    interviewer_name = serializers.CharField(source='interviewer.get_full_name', read_only=True)
    
    class Meta:
        model = Interview
        fields = '__all__'

class OnboardingSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    mentor_name = serializers.CharField(source='mentor.get_full_name', read_only=True)
    
    class Meta:
        model = Onboarding
        fields = '__all__'