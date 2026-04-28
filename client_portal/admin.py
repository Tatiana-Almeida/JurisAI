from django.contrib import admin

from client_portal.models import ClientCaseVisibility, ClientDocumentShare, ClientMessage, ClientPortalAccess


admin.site.register(ClientPortalAccess)
admin.site.register(ClientCaseVisibility)
admin.site.register(ClientDocumentShare)
admin.site.register(ClientMessage)

