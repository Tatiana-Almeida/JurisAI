from django.urls import include, path
from rest_framework.routers import DefaultRouter

from document_analysis.views import (
    AnalysisPlaceholderView,
    DeadlineExtractionRunViewSet,
    DocumentComparisonViewSet,
    DocumentDifferenceViewSet,
    ExtractedDeadlineSuggestionViewSet,
)


router = DefaultRouter()
router.register(r'comparisons', DocumentComparisonViewSet, basename='document-comparison')
router.register(r'differences', DocumentDifferenceViewSet, basename='document-difference')
router.register(r'deadline-runs', DeadlineExtractionRunViewSet, basename='deadline-extraction-run')
router.register(r'deadline-suggestions', ExtractedDeadlineSuggestionViewSet, basename='extracted-deadline-suggestion')

urlpatterns = [
    path('status/', AnalysisPlaceholderView.as_view()),
    path('', include(router.urls)),
]

