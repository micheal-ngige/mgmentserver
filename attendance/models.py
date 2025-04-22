from django.db import models
from accounts.models import User

class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('HALF_DAY', 'Half Day'),
        ('ON_LEAVE', 'On Leave'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABSENT')
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'date')
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"

class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    max_days = models.PositiveIntegerField()
    carry_forward = models.BooleanField(default=False)
    carry_forward_limit = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name} ({self.start_date} to {self.end_date})"