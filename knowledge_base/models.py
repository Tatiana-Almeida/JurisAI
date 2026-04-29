import uuid

from django.conf import settings
from django.db import models


class KnowledgeBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='knowledge_bases')
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='knowledge_bases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return self.name


class KnowledgeDocument(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('document', 'Document'),
        ('manual', 'Manual'),
        ('imported', 'Imported'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('indexed', 'Indexed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='knowledge_documents')
    knowledge_base = models.ForeignKey('knowledge_base.KnowledgeBase', on_delete=models.CASCADE, related_name='documents')
    document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='knowledge_document_links', null=True, blank=True)
    title = models.CharField(max_length=240)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES, default='document')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    indexed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='knowledge_documents',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='document_chunks')
    knowledge_document = models.ForeignKey('knowledge_base.KnowledgeDocument', on_delete=models.CASCADE, related_name='chunks')
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.PROTECT,
        related_name='knowledge_chunks',
        null=True,
        blank=True,
    )
    chunk_index = models.PositiveIntegerField(default=0)
    content = models.TextField()
    content_hash = models.CharField(max_length=64)
    metadata = models.JSONField(default=dict, blank=True)
    char_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chunk_index', 'created_at', 'id']
        unique_together = ('knowledge_document', 'chunk_index')

    def __str__(self):
        return f'{self.knowledge_document.title} #{self.chunk_index}'


class RetrievalQuery(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('no_sources', 'No sources'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='retrieval_queries')
    knowledge_base = models.ForeignKey('knowledge_base.KnowledgeBase', on_delete=models.PROTECT, related_name='queries', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='retrieval_queries')
    query = models.TextField()
    answer = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='no_sources')
    sources_payload = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return self.query[:80]
