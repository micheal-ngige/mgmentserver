from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('HR', 'Human Resource'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

@receiver(post_save, sender=User)
def set_default_department(sender, instance, created, **kwargs):
    if created and not instance.department:
        default_dept = Department.objects.filter(name='Unassigned').first()
        if not default_dept:
            default_dept = Department.objects.create(name='Unassigned', description='Default department for new employees')
        instance.department = default_dept
        instance.save()

# class User(AbstractUser):
#     username = None  # disable username field
#     email = models.EmailField(unique=True)

#     ROLE_CHOICES = (
#         ('HR', 'Human Resource'),
#         ('MANAGER', 'Manager'),
#         ('EMPLOYEE', 'Employee'),
#     )

#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
#     phone = models.CharField(max_length=20, blank=True)
#     address = models.TextField(blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     joining_date = models.DateField(null=True, blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []  # no username required

#     def __str__(self):
#         return f"{self.email} - {self.get_role_display()}"
