from django.contrib import admin
from .models import Project, Task, TaskComment, TaskDelegation

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TaskDelegation)