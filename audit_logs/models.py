import uuid
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='audit_logs',
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50)
    entity = models.CharField(max_length=120)
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.organization_id is None and self.user_id:
            user_organization_id = getattr(self.user, 'organization_id', None)
            if user_organization_id is not None:
                self.organization_id = user_organization_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.action} on {self.entity} at {self.timestamp}'
