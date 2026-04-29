from django.urls import path

from knowledge_base.views import (
    DocumentChunkViewSet,
    EmbeddingAuditLogViewSet,
    IndexingJobViewSet,
    KnowledgeBaseViewSet,
    KnowledgeDocumentViewSet,
    OrganizationRAGSettingsView,
    RetrievalQueryViewSet,
)


knowledge_base_list = KnowledgeBaseViewSet.as_view({'get': 'list', 'post': 'create'})
knowledge_base_detail = KnowledgeBaseViewSet.as_view(
    {'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}
)
knowledge_base_index_document = KnowledgeBaseViewSet.as_view({'post': 'index_document'})
knowledge_base_search = KnowledgeBaseViewSet.as_view({'post': 'search'})
knowledge_base_ask = KnowledgeBaseViewSet.as_view({'post': 'ask'})

knowledge_document_list = KnowledgeDocumentViewSet.as_view({'get': 'list', 'post': 'create'})
knowledge_document_detail = KnowledgeDocumentViewSet.as_view(
    {'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}
)

document_chunk_list = DocumentChunkViewSet.as_view({'get': 'list'})
document_chunk_detail = DocumentChunkViewSet.as_view({'get': 'retrieve'})

retrieval_query_list = RetrievalQueryViewSet.as_view({'get': 'list'})
retrieval_query_detail = RetrievalQueryViewSet.as_view({'get': 'retrieve'})

indexing_job_list = IndexingJobViewSet.as_view({'get': 'list'})
indexing_job_detail = IndexingJobViewSet.as_view({'get': 'retrieve'})
embedding_audit_log_list = EmbeddingAuditLogViewSet.as_view({'get': 'list'})
embedding_audit_log_detail = EmbeddingAuditLogViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('settings/', OrganizationRAGSettingsView.as_view(), name='rag-settings'),
    path('', knowledge_base_list, name='knowledge-base-list'),
    path('<uuid:pk>/', knowledge_base_detail, name='knowledge-base-detail'),
    path('<uuid:pk>/index-document/', knowledge_base_index_document, name='knowledge-base-index-document'),
    path('<uuid:pk>/reindex-document/', KnowledgeBaseViewSet.as_view({'post': 'reindex_document'}), name='knowledge-base-reindex-document'),
    path('<uuid:pk>/prepare-embeddings/', KnowledgeBaseViewSet.as_view({'post': 'prepare_embeddings'}), name='knowledge-base-prepare-embeddings'),
    path('<uuid:pk>/search/', knowledge_base_search, name='knowledge-base-search'),
    path('<uuid:pk>/ask/', knowledge_base_ask, name='knowledge-base-ask'),
    path('<uuid:pk>/stats/', KnowledgeBaseViewSet.as_view({'get': 'stats'}), name='knowledge-base-stats'),
    path('documents/', knowledge_document_list, name='knowledge-document-list'),
    path('documents/<uuid:pk>/', knowledge_document_detail, name='knowledge-document-detail'),
    path('queries/', retrieval_query_list, name='retrieval-query-list'),
    path('queries/<uuid:pk>/', retrieval_query_detail, name='retrieval-query-detail'),
    path('indexing-jobs/', indexing_job_list, name='indexing-job-list'),
    path('indexing-jobs/<uuid:pk>/', indexing_job_detail, name='indexing-job-detail'),
    path('embedding-audit-logs/', embedding_audit_log_list, name='embedding-audit-log-list'),
    path('embedding-audit-logs/<uuid:pk>/', embedding_audit_log_detail, name='embedding-audit-log-detail'),
    path('chunks/', document_chunk_list, name='knowledge-chunk-list'),
    path('chunks/<uuid:pk>/', document_chunk_detail, name='knowledge-chunk-detail'),
    # Backward-compatible aliases from the initial foundation phase.
    path('bases/', knowledge_base_list, name='knowledge-base-list-legacy'),
    path('bases/<uuid:pk>/', knowledge_base_detail, name='knowledge-base-detail-legacy'),
]
