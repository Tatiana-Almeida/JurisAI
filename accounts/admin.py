from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'organization', 'is_active')
    list_filter = ('role', 'organization')
    search_fields = ('email', 'name')
