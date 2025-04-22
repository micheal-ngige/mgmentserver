
from django.db import models
from accounts.models import Department  
from accounts.models import User  

class Team(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_teams')
    members = models.ManyToManyField(User, related_name='teams')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"