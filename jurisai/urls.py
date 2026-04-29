from django.conf import settings
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
    path('health/', health_check, name='healthcheck'),
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
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/client-portal/', include('client_portal.urls')),
    path('api/v1/', include('tasks.urls')),
    path('api/v1/calendar/', include('calendar_events.urls')),
    path('api/v1/', include('legal_templates.urls')),
    path('api/v1/legal-finance/', include('legal_finance.urls')),
    path('api/v1/crm/', include('crm.urls')),
    path('api/v1/signatures/', include('e_signature.urls')),
    path('api/v1/bi/', include('business_intelligence.urls')),
    path('api/v1/compliance/', include('compliance.urls')),
    path('api/v1/marketplace/', include('marketplace.urls')),
    path('api/v1/knowledge-base/', include('knowledge_base.urls')),
    path('api/v1/ocr/', include('ocr.urls')),
    path('api/v1/document-analysis/', include('document_analysis.urls')),
    path('api/v1/health/', health_check),
]

if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
