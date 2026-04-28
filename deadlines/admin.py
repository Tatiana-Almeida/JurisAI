from django.contrib import admin
from deadlines.models import Deadline

@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('law_case', 'due_date', 'completed', 'organization')
    list_filter = ('completed', 'organization')
    search_fields = ('law_case__title',)
