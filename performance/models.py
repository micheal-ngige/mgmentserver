from django.db import models
from accounts.models import Department  
from accounts.models import User

class PerformanceReview(models.Model):
    RATING_CHOICES = (
        (1, 'Poor'),
        (2, 'Needs Improvement'),
        (3, 'Meets Expectations'),
        (4, 'Exceeds Expectations'),
        (5, 'Outstanding'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    review_date = models.DateField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    comments = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_rating_display()} - {self.review_date}"

class KPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  # Fixed reference
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (Target: {self.target}%)"

class UserKPI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.kpi.name} - {self.value}%"