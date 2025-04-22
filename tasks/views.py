from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Project, Task, TaskComment, TaskDelegation
from .serializers import ProjectSerializer, TaskSerializer, TaskCommentSerializer, TaskDelegationSerializer
from accounts.models import User
from django.db.models import Q

class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return Project.objects.all()
        elif user.role == 'MANAGER':
            # Get projects managed by the user or in their department
            return Project.objects.filter(
                Q(manager=user) | Q(team__department=user.department)
            ).distinct()
        else:
            # Get projects where user is a team member
            return Project.objects.filter(
                Q(team__members=user) | Q(tasks__assigned_to=user)
            ).distinct()

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        project_id = self.request.query_params.get('project_id')
        
        queryset = Task.objects.all()
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        if user.role == 'HR':
            return queryset
        elif user.role == 'MANAGER':
            # Get tasks in the manager's department or assigned to their team members
            return queryset.filter(
                Q(project__team__department=user.department) |
                Q(assigned_to__department=user.department)
            ).distinct()
        else:
            # Get tasks assigned to the user or delegated to them
            return queryset.filter(
                Q(assigned_to=user) |
                Q(delegations__to_user=user, delegations__status='APPROVED')
            ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class TaskCommentListView(generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.request.query_params.get('task_id')
        if not task_id:
            return TaskComment.objects.none()
        
        return TaskComment.objects.filter(task_id=task_id).order_by('created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class TaskDelegationListView(generics.ListCreateAPIView):
    serializer_class = TaskDelegationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        task_id = self.request.query_params.get('task_id')
        
        queryset = TaskDelegation.objects.all()
        
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        
        if user.role == 'HR':
            return queryset
        elif user.role == 'MANAGER':

            return queryset.filter(
                Q(task__project__team__department=user.department) |
                Q(from_user__department=user.department) |
                Q(to_user__department=user.department)
            ).distinct()
        else:
            
            return queryset.filter(
                Q(from_user=user) | Q(to_user=user)
            )
    
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class TaskDelegationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskDelegation.objects.all()
    serializer_class = TaskDelegationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ApproveDelegationView(generics.UpdateAPIView):
    queryset = TaskDelegation.objects.all()
    serializer_class = TaskDelegationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role == 'MANAGER' and instance.from_user.department != request.user.department:
            return Response({'detail': 'You can only approve delegations in your department.'}, status=status.HTTP_403_FORBIDDEN)
        
        instance.status = 'APPROVED'
        instance.approved_by = request.user
        instance.save()
        
        # Update the task assignment
        task = instance.task
        task.assigned_to = instance.to_user
        task.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)