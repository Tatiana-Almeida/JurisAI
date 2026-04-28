import uuid
from django.db import models
from django.conf import settings

class LawCase(models.Model):
    STATUS_CHOICES = [
        ('open', 'Aberto'),
        ('in_progress', 'Em andamento'),
        ('closed', 'Encerrado'),
        ('on_hold', 'Pausado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client_cases', on_delete=models.PROTECT)
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lawyer_cases', on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='open')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='cases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
