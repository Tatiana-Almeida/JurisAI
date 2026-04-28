from django.contrib import admin
from documents.models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'law_case', 'version', 'organization', 'created_at')
    list_filter = ('type', 'organization')
    search_fields = ('law_case__title', 'content')
