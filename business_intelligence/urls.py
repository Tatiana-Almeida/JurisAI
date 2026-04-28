from django.urls import include, path
from rest_framework.routers import DefaultRouter

from business_intelligence.views import MetricSnapshotViewSet, ReportDefinitionViewSet, SavedReportViewSet


router = DefaultRouter()
router.register(r'report-definitions', ReportDefinitionViewSet, basename='report-definition')
router.register(r'saved-reports', SavedReportViewSet, basename='saved-report')
router.register(r'metric-snapshots', MetricSnapshotViewSet, basename='metric-snapshot')

urlpatterns = [
    path('', include(router.urls)),
]

