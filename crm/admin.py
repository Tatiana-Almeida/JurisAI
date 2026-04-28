from django.contrib import admin

from crm.models import Consultation, Lead, LeadActivity


admin.site.register(Lead)
admin.site.register(LeadActivity)
admin.site.register(Consultation)

