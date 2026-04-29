from django.contrib import admin

from ocr.models import OCRAuditLog, OCRJob, OCRKnowledgeBasePipelineRun, OCRResult, OCRSettings


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


@admin.register(OCRKnowledgeBasePipelineRun)
class OCRKnowledgeBasePipelineRunAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'knowledge_base',
        'organization',
        'status',
        'step',
        'update_document_content',
        'started_at',
        'finished_at',
        'created_at',
    )
    list_filter = ('organization', 'status', 'step', 'update_document_content', 'created_at')
    search_fields = ('document__id', 'knowledge_base__name', 'error_message')


@admin.register(OCRSettings)
class OCRSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'organization',
        'advanced_ocr_enabled',
        'external_ocr_enabled',
        'preferred_ocr_provider',
        'image_ocr_mode',
        'scanned_pdf_ocr_mode',
        'updated_at',
    )
    list_filter = (
        'advanced_ocr_enabled',
        'external_ocr_enabled',
        'preferred_ocr_provider',
        'image_ocr_mode',
        'scanned_pdf_ocr_mode',
    )
    search_fields = ('organization__name',)


@admin.register(OCRAuditLog)
class OCRAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'organization',
        'document',
        'ocr_job',
        'action',
        'provider',
        'mode',
        'status',
        'reason',
        'created_at',
    )
    list_filter = ('organization', 'provider', 'mode', 'action', 'status', 'created_at')
    search_fields = ('document__id', 'reason')
