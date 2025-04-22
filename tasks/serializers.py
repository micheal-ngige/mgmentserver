from rest_framework import serializers
from .models import Project, Task, TaskComment, TaskDelegation

class ProjectSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    department_name = serializers.CharField(source='team.department.name', read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = TaskComment
        fields = '__all__'

class TaskDelegationSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    from_user_name = serializers.CharField(source='from_user.get_full_name', read_only=True)
    to_user_name = serializers.CharField(source='to_user.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = TaskDelegation
        fields = '__all__'