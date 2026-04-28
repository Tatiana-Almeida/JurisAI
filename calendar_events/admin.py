from django.contrib import admin

from calendar_events.models import CalendarEvent, EventAttendee, EventReminder


admin.site.register(CalendarEvent)
admin.site.register(EventReminder)
admin.site.register(EventAttendee)

