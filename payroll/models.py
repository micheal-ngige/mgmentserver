from django.db import models
from accounts.models import User

class Payroll(models.Model):
    REMUNERATION_TYPE = (
        ('SALARY', 'Base Salary'),
        ('BONUS', 'Bonus'),
        ('ALLOWANCE', 'Allowance'),
        ('DEDUCTION', 'Deduction'),
    )
    
    FREQUENCY_CHOICES = (
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
        ('QUARTERLY', 'Quarterly'),
        ('ONE_TIME', 'One Time'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=REMUNERATION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    effective_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()} - {self.amount}"

class Payslip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year} - {self.net_salary}"

class TaxConfiguration(models.Model):
    name = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.tax_percentage}%"