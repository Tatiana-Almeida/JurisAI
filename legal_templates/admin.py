from django.contrib import admin

from legal_templates.models import GeneratedDocument, LegalTemplate, TemplateCategory, TemplateVariable


admin.site.register(TemplateCategory)
admin.site.register(LegalTemplate)
admin.site.register(TemplateVariable)
admin.site.register(GeneratedDocument)

