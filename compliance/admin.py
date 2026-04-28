from django.contrib import admin

from compliance.models import (
    AccessLog,
    DataConsent,
    DataDeletionRequest,
    DataExportRequest,
    DataRetentionPolicy,
    SensitiveDataFlag,
)


admin.site.register(DataConsent)
admin.site.register(DataRetentionPolicy)
admin.site.register(SensitiveDataFlag)
admin.site.register(DataExportRequest)
admin.site.register(DataDeletionRequest)
admin.site.register(AccessLog)

