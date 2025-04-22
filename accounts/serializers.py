from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from departments.models import Team
from .models import Department


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    teams = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'department', 'department_name', 'phone', 'address', 'date_of_birth',
                 'joining_date', 'profile_picture', 'teams']
        extra_kwargs = {
            'password': {'write_only': True},
            'department': {'write_only': True},
        }
    
    def get_teams(self, obj):
        return [team.name for team in obj.teams.all()]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'user': UserSerializer(user).data,
            'role': user.role,
        })
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'

