from django.contrib import admin
from .models import PerformanceReview, KPI, UserKPI

admin.site.register(PerformanceReview)
admin.site.register(KPI)
admin.site.register(UserKPI)