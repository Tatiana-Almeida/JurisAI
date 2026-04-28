from django.urls import path, include
from rest_framework.routers import DefaultRouter
from deadlines.views import DeadlineViewSet

router = DefaultRouter()
router.register(r'deadlines', DeadlineViewSet, basename='deadline')

urlpatterns = [
    path('', include(router.urls)),
]
