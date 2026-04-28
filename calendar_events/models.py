import uuid

from django.conf import settings
from django.db import models


class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('deadline', 'Deadline'),
        ('hearing', 'Hearing'),
        ('meeting', 'Meeting'),
        ('task', 'Task'),
        ('financial', 'Financial'),
        ('custom', 'Custom'),
    ]
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='calendar_events')
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.PROTECT, related_name='calendar_events', null=True, blank=True)
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='custom')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    location = models.CharField(max_length=240, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_calendar_events')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assigned_calendar_events', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_at', 'created_at']


class EventReminder(models.Model):
    CHANNEL_CHOICES = [('email', 'Email'), ('whatsapp', 'WhatsApp'), ('in_app', 'In App')]
    STATUS_CHOICES = [('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='event_reminders')
    event = models.ForeignKey('calendar_events.CalendarEvent', on_delete=models.CASCADE, related_name='reminders')
    remind_at = models.DateTimeField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


class EventAttendee(models.Model):
    ATTENDANCE_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('tentative', 'Tentative')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='event_attendees')
    event = models.ForeignKey('calendar_events.CalendarEvent', on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='event_attendances')
    attendance_status = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES, default='pending')

    class Meta:
        unique_together = ('organization', 'event', 'user')

