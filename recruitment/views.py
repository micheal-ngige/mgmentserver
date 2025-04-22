from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import JobPosition, Applicant, Interview, Onboarding
from .serializers import JobPositionSerializer, ApplicantSerializer, InterviewSerializer, OnboardingSerializer
from accounts.models import User
from django.db.models import Q

class JobPositionListView(generics.ListCreateAPIView):
    queryset = JobPosition.objects.filter(is_active=True)
    serializer_class = JobPositionSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobPositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class ApplicantListView(generics.ListCreateAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status')
        
        queryset = Applicant.objects.all()
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if user.role == 'HR':
            return queryset
        elif user.role == 'MANAGER':
            # Get applicants for positions in the manager's department
            return queryset.filter(
                Q(position__department=user.department) |
                Q(assigned_to=user)
            ).distinct()
        else:
            return queryset.filter(assigned_to=user)

class ApplicantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class UpdateApplicantStatusView(generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'detail': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_status not in dict(Applicant.STATUS_CHOICES).keys():
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = new_status
        instance.save()
        
        # If status is HIRED, create onboarding record
        if new_status == 'HIRED' and not hasattr(instance, 'onboarding'):
            Onboarding.objects.create(
                applicant=instance,
                start_date=request.data.get('start_date'),
                end_date=request.data.get('end_date'),
                mentor=request.data.get('mentor_id') and User.objects.get(id=request.data.get('mentor_id'))
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class InterviewListView(generics.ListCreateAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        applicant_id = self.request.query_params.get('applicant_id')
        
        queryset = Interview.objects.all()
        
        if applicant_id:
            queryset = queryset.filter(applicant_id=applicant_id)
        
        if user.role == 'HR':
            return queryset
        elif user.role == 'MANAGER':
            # Get interviews for applicants in the manager's department or where they are the interviewer
            return queryset.filter(
                Q(applicant__position__department=user.department) |
                Q(interviewer=user)
            ).distinct()
        else:
            return queryset.filter(interviewer=user)
    
    def perform_create(self, serializer):
        serializer.save(interviewer=self.request.user)

class InterviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class OnboardingListView(generics.ListAPIView):
    serializer_class = OnboardingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status')
        
        queryset = Onboarding.objects.all()
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if user.role == 'HR':
            return queryset
        elif user.role == 'MANAGER':
            # Get onboarding for applicants in the manager's department or where they are the mentor
            return queryset.filter(
                Q(applicant__position__department=user.department) |
                Q(mentor=user)
            ).distinct()
        else:
            return queryset.filter(mentor=user)

class OnboardingDetailView(generics.RetrieveUpdateAPIView):
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class UpdateOnboardingStatusView(generics.UpdateAPIView):
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'detail': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_status not in dict(Onboarding.STATUS_CHOICES).keys():
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = new_status
        instance.save()
        

        if new_status == 'COMPLETED' and not instance.applicant.user:
            user = User.objects.create_user(
                username=instance.applicant.email.split('@')[0],
                email=instance.applicant.email,
                first_name=instance.applicant.first_name,
                last_name=instance.applicant.last_name,
                role='EMPLOYEE',
                department=instance.applicant.position.department,
                password='defaultpassword'  
            )
            instance.applicant.user = user
            instance.applicant.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)