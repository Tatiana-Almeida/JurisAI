from django.urls import path, include
from rest_framework.routers import DefaultRouter
from law_cases.views import LawCaseViewSet

router = DefaultRouter()
router.register(r'cases', LawCaseViewSet, basename='lawcase')

urlpatterns = [
    path('', include(router.urls)),
]
