from django.contrib import admin

from document_analysis.models import (
    DeadlineExtractionRun,
    DocumentComparison,
    DocumentDifference,
    ExtractedDeadlineSuggestion,
)


admin.site.register(DocumentComparison)
admin.site.register(DocumentDifference)
admin.site.register(DeadlineExtractionRun)
admin.site.register(ExtractedDeadlineSuggestion)

