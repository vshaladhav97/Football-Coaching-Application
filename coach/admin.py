from django.contrib import admin
from .models import Coach, CoachDocuments
# Register your models here.


class CoachAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'landline', 'address', 'postal_code']


admin.site.register(Coach, CoachAdmin)
admin.site.register(CoachDocuments)