from django.urls import include, path
from rest_framework.routers import DefaultRouter

from crm.views import ConsultationViewSet, LeadActivityViewSet, LeadViewSet


router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='crm-lead')
router.register(r'lead-activities', LeadActivityViewSet, basename='crm-lead-activity')
router.register(r'consultations', ConsultationViewSet, basename='crm-consultation')

urlpatterns = [
    path('', include(router.urls)),
]

