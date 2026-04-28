import uuid
from django.db import models
from jurisai.utils import document_upload_path

class Document(models.Model):
    TYPE_CHOICES = [
        ('petition', 'Petição'),
        ('contract', 'Contrato'),
        ('evidence', 'Prova'),
        ('internal', 'Documento interno'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.CASCADE, related_name='documents')
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to=document_upload_path, blank=True, null=True)
    version = models.PositiveIntegerField(default=1)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('law_case', 'version')
        ordering = ['-version', '-created_at']

    def __str__(self):
        return f'{self.type} - {self.law_case.title} (v{self.version})'
