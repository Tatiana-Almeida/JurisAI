import uuid
from django.db import models

class Deadline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.CASCADE, related_name='deadlines')
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='deadlines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.law_case.title} - {self.due_date.isoformat()}'
