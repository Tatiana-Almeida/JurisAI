import uuid

from django.conf import settings
from django.db import models


class TemplatePublisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='marketplace_publishers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='marketplace_publishers')
    display_name = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)


class MarketplaceTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='marketplace_templates')
    publisher = models.ForeignKey('marketplace.TemplatePublisher', on_delete=models.PROTECT, related_name='templates')
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TemplatePurchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='template_purchases')
    marketplace_template = models.ForeignKey('marketplace.MarketplaceTemplate', on_delete=models.PROTECT, related_name='purchases')
    purchased_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='template_purchases')
    created_at = models.DateTimeField(auto_now_add=True)


class TemplateReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='template_reviews')
    marketplace_template = models.ForeignKey('marketplace.MarketplaceTemplate', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='template_reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

