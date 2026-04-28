from django.urls import include, path
from rest_framework.routers import DefaultRouter

from knowledge_base.views import (
    DocumentChunkViewSet,
    KnowledgeBaseSearchPlaceholderView,
    KnowledgeBaseViewSet,
    KnowledgeDocumentViewSet,
    RetrievalQueryViewSet,
)


router = DefaultRouter()
router.register(r'bases', KnowledgeBaseViewSet, basename='knowledge-base')
router.register(r'documents', KnowledgeDocumentViewSet, basename='knowledge-document')
router.register(r'chunks', DocumentChunkViewSet, basename='knowledge-chunk')
router.register(r'queries', RetrievalQueryViewSet, basename='retrieval-query')

urlpatterns = [
    path('search/', KnowledgeBaseSearchPlaceholderView.as_view()),
    path('', include(router.urls)),
]

