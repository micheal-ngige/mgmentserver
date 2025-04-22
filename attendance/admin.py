from django.contrib import admin
from .models import Shift, Attendance, LeaveType, LeaveRequest

admin.site.register(Shift)
admin.site.register(Attendance)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)