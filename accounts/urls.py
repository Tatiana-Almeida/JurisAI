from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, RegisterView, MeView, ChangePasswordView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', RegisterView.as_view(), name='user_register'),
    path('users/me/', MeView.as_view(), name='user_me'),
    path('users/change-password/', ChangePasswordView.as_view(), name='user_change_password'),
]
