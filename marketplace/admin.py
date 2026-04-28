from django.contrib import admin

from marketplace.models import MarketplaceTemplate, TemplatePublisher, TemplatePurchase, TemplateReview


admin.site.register(TemplatePublisher)
admin.site.register(MarketplaceTemplate)
admin.site.register(TemplatePurchase)
admin.site.register(TemplateReview)

