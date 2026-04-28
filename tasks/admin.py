from django.contrib import admin

from tasks.models import Task, TaskChecklistItem, TaskComment


admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TaskChecklistItem)

