import uuid
from django.db import models

class Organization(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('solo', 'Solo'),
        ('growth', 'Escritório'),
        ('enterprise', 'Enterprise'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=180, unique=True)
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default='free')
    created_at = models.DateTimeField(auto_now_add=True)

    def max_users(self):
        return {
            'free': 1,
            'solo': 1,
            'growth': 10,
            'enterprise': 9999,
        }.get(self.plan, 1)

    def max_cases(self):
        return {
            'free': 10,
            'solo': 100,
            'growth': 9999,
            'enterprise': 9999,
        }.get(self.plan, 10)

    def max_documents(self):
        return {
            'free': 50,
            'solo': 500,
            'growth': 9999,
            'enterprise': 9999,
        }.get(self.plan, 50)

    def ai_request_limit(self):
        return {
            'free': 20,
            'solo': 100,
            'growth': 500,
            'enterprise': 2000,
        }.get(self.plan, 20)

    def can_add_user(self):
        return self.users.count() < self.max_users()

    def __str__(self):
        return self.name
