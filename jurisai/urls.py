from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from jurisai.health import health_check

schema_view = get_schema_view(
    openapi.Info(
        title='JurisAI API',
        default_version='v1',
        description='API para plataforma SaaS jurídica com suporte multi-tenant e IA',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('organizations.urls')),
    path('api/v1/', include('law_cases.urls')),
    path('api/v1/', include('deadlines.urls')),
    path('api/v1/', include('documents.urls')),
    path('api/v1/', include('billing.urls')),
    path('api/v1/', include('audit_logs.urls')),
    path('api/v1/', include('notifications.urls')),
    path('api/v1/ai/', include('ai_assistant.urls')),
    path('api/v1/health/', health_check),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
