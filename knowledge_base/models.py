import uuid

from django.conf import settings
from django.db import models


class KnowledgeBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='knowledge_bases')
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='knowledge_bases')
    created_at = models.DateTimeField(auto_now_add=True)


class KnowledgeDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='knowledge_documents')
    knowledge_base = models.ForeignKey('knowledge_base.KnowledgeBase', on_delete=models.CASCADE, related_name='documents')
    document = models.ForeignKey('documents.Document', on_delete=models.PROTECT, related_name='knowledge_document_links', null=True, blank=True)
    title = models.CharField(max_length=240)
    status = models.CharField(max_length=30, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='document_chunks')
    knowledge_document = models.ForeignKey('knowledge_base.KnowledgeDocument', on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.PositiveIntegerField(default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class RetrievalQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='retrieval_queries')
    knowledge_base = models.ForeignKey('knowledge_base.KnowledgeBase', on_delete=models.PROTECT, related_name='queries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='retrieval_queries')
    query = models.TextField()
    status = models.CharField(max_length=30, default='not_implemented')
    created_at = models.DateTimeField(auto_now_add=True)

