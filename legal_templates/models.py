import uuid

from django.conf import settings
from django.db import models


class TemplateCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='template_categories')
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'name')


class LegalTemplate(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('petition', 'Petition'),
        ('contract', 'Contract'),
        ('power_of_attorney', 'Power of Attorney'),
        ('notice', 'Notice'),
        ('opinion', 'Opinion'),
        ('agreement', 'Agreement'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='legal_templates')
    category = models.ForeignKey('legal_templates.TemplateCategory', on_delete=models.PROTECT, related_name='templates', null=True, blank=True)
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES, default='other')
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_legal_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class TemplateVariable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='template_variables')
    template = models.ForeignKey('legal_templates.LegalTemplate', on_delete=models.CASCADE, related_name='variables')
    name = models.CharField(max_length=120)
    label = models.CharField(max_length=180)
    required = models.BooleanField(default=False)
    default_value = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('organization', 'template', 'name')


class GeneratedDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='generated_documents')
    template = models.ForeignKey('legal_templates.LegalTemplate', on_delete=models.PROTECT, related_name='generated_documents')
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.PROTECT, related_name='generated_documents', null=True, blank=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='generated_documents')
    rendered_content = models.TextField()
    variables_payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

