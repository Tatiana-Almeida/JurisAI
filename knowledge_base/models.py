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
    EMBEDDING_STATUS_CHOICES = [
        ('not_generated', 'Not generated'),
        ('generated', 'Generated'),
        ('failed', 'Failed'),
    ]

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
    embedding_status = models.CharField(max_length=20, choices=EMBEDDING_STATUS_CHOICES, default='not_generated')
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
    retrieval_method = models.CharField(max_length=30, default='textual')
    confidence = models.CharField(max_length=20, default='low')
    sources_count = models.PositiveIntegerField(default=0)
    sources_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return self.query[:80]


class IndexingJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='knowledge_indexing_jobs')
    knowledge_base = models.ForeignKey('knowledge_base.KnowledgeBase', on_delete=models.PROTECT, related_name='indexing_jobs')
    knowledge_document = models.ForeignKey(
        'knowledge_base.KnowledgeDocument',
        on_delete=models.PROTECT,
        related_name='indexing_jobs',
        null=True,
        blank=True,
    )
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.PROTECT,
        related_name='knowledge_indexing_jobs',
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    chunks_created = models.PositiveIntegerField(default=0)
    chunks_deleted = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='knowledge_indexing_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.knowledge_base.name} - {self.status}'


class ChunkEmbedding(models.Model):
    STATUS_CHOICES = [
        ('not_generated', 'Not generated'),
        ('generated', 'Generated'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='chunk_embeddings')
    chunk = models.OneToOneField('knowledge_base.DocumentChunk', on_delete=models.CASCADE, related_name='embedding')
    provider = models.CharField(max_length=120, blank=True)
    model = models.CharField(max_length=120, blank=True)
    vector = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_generated')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.chunk_id} - {self.status}'
