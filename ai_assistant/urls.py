from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ai_assistant.views import (
    GeneratePetitionView,
    SummarizeDocumentView,
    AnalyzeRiskView,
    SearchJurisprudenceView,
    DraftContractView,
    ReviewDocumentView,
    AIRequestViewSet,
)

router = DefaultRouter()
router.register(r'history', AIRequestViewSet, basename='ai_history')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-petition/', GeneratePetitionView.as_view(), name='generate_petition'),
    path('summarize-document/', SummarizeDocumentView.as_view(), name='summarize_document'),
    path('analyze-risk/', AnalyzeRiskView.as_view(), name='analyze_risk'),
    path('search-jurisprudence/', SearchJurisprudenceView.as_view(), name='search_jurisprudence'),
    path('draft-contract/', DraftContractView.as_view(), name='draft_contract'),
    path('review-document/', ReviewDocumentView.as_view(), name='review_document'),
]
