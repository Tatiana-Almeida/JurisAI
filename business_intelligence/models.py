import uuid

from django.conf import settings
from django.db import models


class ReportDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='report_definitions')
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=180)
    config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'slug')


class SavedReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='saved_reports')
    report_definition = models.ForeignKey('business_intelligence.ReportDefinition', on_delete=models.PROTECT, related_name='saved_reports')
    saved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='saved_reports')
    parameters = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MetricSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='metric_snapshots')
    metric_key = models.CharField(max_length=120)
    metric_value = models.DecimalField(max_digits=14, decimal_places=2)
    captured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

