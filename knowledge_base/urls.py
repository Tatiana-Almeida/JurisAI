from django.urls import path

from knowledge_base.views import (
    DocumentChunkViewSet,
    KnowledgeBaseViewSet,
    KnowledgeDocumentViewSet,
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

urlpatterns = [
    path('', knowledge_base_list, name='knowledge-base-list'),
    path('<uuid:pk>/', knowledge_base_detail, name='knowledge-base-detail'),
    path('<uuid:pk>/index-document/', knowledge_base_index_document, name='knowledge-base-index-document'),
    path('<uuid:pk>/search/', knowledge_base_search, name='knowledge-base-search'),
    path('<uuid:pk>/ask/', knowledge_base_ask, name='knowledge-base-ask'),
    path('documents/', knowledge_document_list, name='knowledge-document-list'),
    path('documents/<uuid:pk>/', knowledge_document_detail, name='knowledge-document-detail'),
    path('queries/', retrieval_query_list, name='retrieval-query-list'),
    path('queries/<uuid:pk>/', retrieval_query_detail, name='retrieval-query-detail'),
    path('chunks/', document_chunk_list, name='knowledge-chunk-list'),
    path('chunks/<uuid:pk>/', document_chunk_detail, name='knowledge-chunk-detail'),
    # Backward-compatible aliases from the initial foundation phase.
    path('bases/', knowledge_base_list, name='knowledge-base-list-legacy'),
    path('bases/<uuid:pk>/', knowledge_base_detail, name='knowledge-base-detail-legacy'),
]
