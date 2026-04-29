import uuid

from django.conf import settings
from django.db import models


class OCRJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    EXTRACTION_METHOD_CHOICES = [
        ('txt', 'TXT'),
        ('pdf_text', 'PDF text'),
        ('docx_text', 'DOCX text'),
        ('image_local', 'Local image OCR'),
        ('scanned_pdf_local', 'Local scanned PDF OCR'),
        ('unsupported', 'Unsupported'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='ocr_jobs')
    document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='ocr_jobs', null=True, blank=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ocr_jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    extraction_method = models.CharField(max_length=20, choices=EXTRACTION_METHOD_CHOICES, default='unsupported')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.document_id} - {self.status}'


class OCRResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='ocr_results')
    job = models.ForeignKey('ocr.OCRJob', on_delete=models.CASCADE, related_name='results')
    document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='ocr_results', null=True, blank=True)
    extracted_text = models.TextField(blank=True)
    char_count = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.document_id} - {self.char_count}'


class OCRPageResult(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='ocr_page_results')
    ocr_result = models.ForeignKey('ocr.OCRResult', on_delete=models.CASCADE, related_name='page_results')
    ocr_job = models.ForeignKey('ocr.OCRJob', on_delete=models.CASCADE, related_name='page_results')
    document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='ocr_page_results')
    page_number = models.PositiveIntegerField()
    extracted_text = models.TextField(blank=True)
    char_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['page_number', 'created_at', 'id']

    def __str__(self):
        return f'{self.document_id} - pagina {self.page_number} - {self.status}'


class OCRKnowledgeBasePipelineRun(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    STEP_CHOICES = [
        ('started', 'Started'),
        ('ocr', 'OCR'),
        ('apply_to_document', 'Apply to document'),
        ('index_document', 'Index document'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='ocr_knowledge_base_pipeline_runs',
    )
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.PROTECT,
        related_name='ocr_knowledge_base_pipeline_runs',
    )
    knowledge_base = models.ForeignKey(
        'knowledge_base.KnowledgeBase',
        on_delete=models.PROTECT,
        related_name='ocr_pipeline_runs',
    )
    ocr_job = models.ForeignKey(
        'ocr.OCRJob',
        on_delete=models.SET_NULL,
        related_name='knowledge_base_pipeline_runs',
        null=True,
        blank=True,
    )
    ocr_result = models.ForeignKey(
        'ocr.OCRResult',
        on_delete=models.SET_NULL,
        related_name='knowledge_base_pipeline_runs',
        null=True,
        blank=True,
    )
    knowledge_document = models.ForeignKey(
        'knowledge_base.KnowledgeDocument',
        on_delete=models.SET_NULL,
        related_name='ocr_pipeline_runs',
        null=True,
        blank=True,
    )
    indexing_job = models.ForeignKey(
        'knowledge_base.IndexingJob',
        on_delete=models.SET_NULL,
        related_name='ocr_pipeline_runs',
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    step = models.CharField(max_length=30, choices=STEP_CHOICES, default='started')
    update_document_content = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ocr_knowledge_base_pipeline_runs',
    )
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.document_id} -> {self.knowledge_base_id} [{self.status}]'


class OCRSettings(models.Model):
    OCR_PROVIDER_CHOICES = [
        ('local', 'Local'),
        ('tesseract', 'Tesseract'),
        ('google_vision', 'Google Vision'),
        ('azure_vision', 'Azure Vision'),
        ('aws_textract', 'AWS Textract'),
        ('other', 'Other'),
    ]
    OCR_MODE_CHOICES = [
        ('disabled', 'Disabled'),
        ('local', 'Local'),
        ('local_placeholder', 'Local placeholder'),
        ('external', 'External'),
    ]

    organization = models.OneToOneField(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='ocr_settings',
    )
    advanced_ocr_enabled = models.BooleanField(default=False)
    external_ocr_enabled = models.BooleanField(default=False)
    allow_document_content_to_external_ocr_provider = models.BooleanField(default=False)
    preferred_ocr_provider = models.CharField(max_length=40, choices=OCR_PROVIDER_CHOICES, default='local')
    preferred_ocr_model = models.CharField(max_length=120, blank=True)
    image_ocr_mode = models.CharField(max_length=30, choices=OCR_MODE_CHOICES, default='disabled')
    scanned_pdf_ocr_mode = models.CharField(max_length=30, choices=OCR_MODE_CHOICES, default='disabled')
    max_scanned_pdf_pages = models.PositiveIntegerField(default=10)
    max_ocr_file_size_mb = models.PositiveIntegerField(default=25)
    max_ocr_chars_output = models.PositiveIntegerField(default=200000)
    store_page_level_ocr = models.BooleanField(default=True)
    require_human_review = models.BooleanField(default=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ocr_settings_updates',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['organization_id']

    def __str__(self):
        return f'OCR settings - {self.organization_id}'


class OCRAuditLog(models.Model):
    ACTION_CHOICES = [
        ('requested', 'Requested'),
        ('skipped', 'Skipped'),
        ('failed', 'Failed'),
        ('completed', 'Completed'),
    ]
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('skipped', 'Skipped'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='ocr_audit_logs',
    )
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        related_name='ocr_audit_logs',
        null=True,
        blank=True,
    )
    ocr_job = models.ForeignKey(
        'ocr.OCRJob',
        on_delete=models.SET_NULL,
        related_name='audit_logs',
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    provider = models.CharField(max_length=120, blank=True)
    mode = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ok')
    reason = models.CharField(max_length=120, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ocr_audit_logs',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.organization_id} - {self.action} - {self.reason}'
