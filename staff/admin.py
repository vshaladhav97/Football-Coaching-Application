from django.contrib import admin
from .models import Staff


class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'landline', 'address', 'postal_code']


admin.site.register(Staff, StaffAdmin)
