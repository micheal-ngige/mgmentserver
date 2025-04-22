from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Shift, Attendance, LeaveType, LeaveRequest
from .serializers import ShiftSerializer, AttendanceSerializer, LeaveTypeSerializer, LeaveRequestSerializer
from django.utils import timezone
from django.db.models import Q
from accounts.models import User

class ShiftListView(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class ShiftDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return Attendance.objects.all()
        elif user.role == 'MANAGER':
            # Get attendance for users in the manager's department
            return Attendance.objects.filter(user__department=user.department)
        else:
            return Attendance.objects.filter(user=user)

class AttendanceDetailView(generics.RetrieveUpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class CheckInView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        today = timezone.now().date()
        existing_attendance = Attendance.objects.filter(user=request.user, date=today).first()
        
        if existing_attendance and existing_attendance.check_in:
            return Response({'detail': 'You have already checked in today.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if existing_attendance:
            existing_attendance.check_in = timezone.now()
            existing_attendance.save()
            serializer = self.get_serializer(existing_attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        data = {
            'user': request.user.id,
            'date': today,
            'check_in': timezone.now(),
            'status': 'PRESENT'
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckOutView(generics.UpdateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        today = timezone.now().date()
        return Attendance.objects.get(user=self.request.user, date=today)
    
    def update(self, request, *args, **kwargs):
        attendance = self.get_object()
        
        if not attendance.check_in:
            return Response({'detail': 'You need to check in first.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if attendance.check_out:
            return Response({'detail': 'You have already checked out today.'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance.check_out = timezone.now()
        attendance.save()
        serializer = self.get_serializer(attendance)
        return Response(serializer.data)

class LeaveTypeListView(generics.ListCreateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class LeaveTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class LeaveRequestListView(generics.ListCreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'HR':
            return LeaveRequest.objects.all()
        elif user.role == 'MANAGER':
            # Get leave requests for users in the manager's department
            return LeaveRequest.objects.filter(user__department=user.department)
        else:
            return LeaveRequest.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LeaveRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ApproveLeaveView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role == 'MANAGER' and instance.user.department != request.user.department:
            return Response({'detail': 'You can only approve leaves for your department.'}, status=status.HTTP_403_FORBIDDEN)
        
        instance.status = 'APPROVED'
        instance.approved_by = request.user
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RejectLeaveView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role == 'MANAGER' and instance.user.department != request.user.department:
            return Response({'detail': 'You can only reject leaves for your department.'}, status=status.HTTP_403_FORBIDDEN)
        
        rejection_reason = request.data.get('rejection_reason', '')
        if not rejection_reason:
            return Response({'detail': 'Rejection reason is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = 'REJECTED'
        instance.rejection_reason = rejection_reason
        instance.approved_by = request.user
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)