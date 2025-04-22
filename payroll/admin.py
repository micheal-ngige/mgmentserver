from django.contrib import admin
from .models import Payroll, Payslip, TaxConfiguration

admin.site.register(Payroll)
admin.site.register(Payslip)
admin.site.register(TaxConfiguration)