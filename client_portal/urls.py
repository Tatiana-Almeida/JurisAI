from django.urls import include, path
from rest_framework.routers import DefaultRouter

from client_portal.views import (
    ClientCaseVisibilityViewSet,
    ClientDocumentShareViewSet,
    ClientPortalCasesView,
    ClientPortalDocumentsView,
    ClientPortalMessagesView,
)


router = DefaultRouter()
router.register(r'case-visibility', ClientCaseVisibilityViewSet, basename='client-case-visibility')
router.register(r'document-shares', ClientDocumentShareViewSet, basename='client-document-share')

urlpatterns = [
    path('cases/', ClientPortalCasesView.as_view()),
    path('documents/', ClientPortalDocumentsView.as_view()),
    path('messages/', ClientPortalMessagesView.as_view()),
    path('', include(router.urls)),
]

