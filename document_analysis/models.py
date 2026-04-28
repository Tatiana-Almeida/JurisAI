import uuid

from django.conf import settings
from django.db import models


class DocumentComparison(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='document_comparisons')
    left_document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='left_document_comparisons')
    right_document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='right_document_comparisons')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='document_comparisons')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class DocumentDifference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='document_differences')
    comparison = models.ForeignKey('document_analysis.DocumentComparison', on_delete=models.CASCADE, related_name='differences')
    difference_type = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class DeadlineExtractionRun(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='deadline_extraction_runs')
    document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='deadline_extraction_runs')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='deadline_extraction_runs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class ExtractedDeadlineSuggestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='extracted_deadline_suggestions')
    extraction_run = models.ForeignKey('document_analysis.DeadlineExtractionRun', on_delete=models.CASCADE, related_name='suggestions')
    suggested_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

