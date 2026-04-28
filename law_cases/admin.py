from django.contrib import admin
from law_cases.models import LawCase

@admin.register(LawCase)
class LawCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'organization', 'lawyer', 'client', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'organization')
