from django.contrib import admin
from .models import JobPosition, Applicant, Interview, Onboarding

admin.site.register(JobPosition)
admin.site.register(Applicant)
admin.site.register(Interview)
admin.site.register(Onboarding)