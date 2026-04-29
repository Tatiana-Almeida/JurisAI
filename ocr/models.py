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
