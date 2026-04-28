from django.urls import include, path
from rest_framework.routers import DefaultRouter

from marketplace.views import (
    MarketplaceTemplateViewSet,
    TemplatePublisherViewSet,
    TemplatePurchaseViewSet,
    TemplateReviewViewSet,
)


router = DefaultRouter()
router.register(r'publishers', TemplatePublisherViewSet, basename='marketplace-publisher')
router.register(r'templates', MarketplaceTemplateViewSet, basename='marketplace-template')
router.register(r'purchases', TemplatePurchaseViewSet, basename='template-purchase')
router.register(r'reviews', TemplateReviewViewSet, basename='template-review')

urlpatterns = [
    path('', include(router.urls)),
]

