from django.contrib import admin

from ocr.models import OCRJob, OCRResult


@admin.register(OCRJob)
class OCRJobAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'organization',
        'requested_by',
        'status',
        'extraction_method',
        'started_at',
        'finished_at',
        'created_at',
    )
    list_filter = ('organization', 'status', 'extraction_method', 'created_at')
    search_fields = ('document__id', 'error_message')


@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ('document', 'organization', 'char_count', 'created_at')
    list_filter = ('organization', 'created_at')
    search_fields = ('document__id', 'extracted_text')
