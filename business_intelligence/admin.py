from django.contrib import admin

from business_intelligence.models import MetricSnapshot, ReportDefinition, SavedReport


admin.site.register(ReportDefinition)
admin.site.register(SavedReport)
admin.site.register(MetricSnapshot)

