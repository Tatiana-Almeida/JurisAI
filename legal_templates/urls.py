from django.urls import include, path
from rest_framework.routers import DefaultRouter

from legal_templates.views import GeneratedDocumentViewSet, LegalTemplateViewSet, TemplateCategoryViewSet


router = DefaultRouter()
router.register(r'legal-template-categories', TemplateCategoryViewSet, basename='template-category')
router.register(r'legal-templates', LegalTemplateViewSet, basename='legal-template')
router.register(r'generated-documents', GeneratedDocumentViewSet, basename='generated-document')

urlpatterns = [
    path('', include(router.urls)),
]

