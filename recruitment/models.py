from django.db import models
from accounts.models import Department  
from accounts.models import User 

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Fixed reference
    description = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Applicant(models.Model):
    STATUS_CHOICES = (
        ('APPLIED', 'Applied'),
        ('SCREENING', 'Screening'),
        ('INTERVIEW', 'Interview'),
        ('OFFER', 'Offer'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    applied_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position.title}"

class Interview(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Applicant.STATUS_CHOICES, default='INTERVIEW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant} - {self.interview_date}"

class Onboarding(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=(
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ), default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant} - {self.status}"