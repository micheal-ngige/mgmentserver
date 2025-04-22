from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import PerformanceReview, KPI, UserKPI
from .serializers import PerformanceReviewSerializer, KPISerializer, UserKPISerializer
from accounts.models import User
from django.db.models import Q

class PerformanceReviewListView(generics.ListCreateAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return PerformanceReview.objects.all()
        elif user.role == 'MANAGER':
            # Get reviews for users in the manager's department
            return PerformanceReview.objects.filter(user__department=user.department)
        else:
            return PerformanceReview.objects.filter(Q(user=user) | Q(reviewer=user))

class PerformanceReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ApprovePerformanceReviewView(generics.UpdateAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_approved = True
        instance.approved_by = request.user
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class KPIListView(generics.ListCreateAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [permissions.IsAuthenticated]

class KPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class UserKPIListView(generics.ListCreateAPIView):
    serializer_class = UserKPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return UserKPI.objects.all()
        elif user.role == 'MANAGER':
            # Get KPIs for users in the manager's department
            return UserKPI.objects.filter(user__department=user.department)
        else:
            return UserKPI.objects.filter(user=user)

class UserKPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserKPI.objects.all()
    serializer_class = UserKPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]