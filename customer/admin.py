from django.contrib import admin
from .models import (Role, User, Customer, Student, RolePermissions, Payment)
# Register your models here.


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_id', 'amount', 'total_amount', 'status',
                    'Payment_gateway_reference_id', 'created_at', 'updated_at']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'first_name', 'last_name',
                    'date_joined', 'is_active', 'is_staff', 'avatar']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name',
                    'email', 'landline', 'address', 'postal_code']


class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", 'first_name', 'last_name', 'age', 'school_name']

@admin.register(RolePermissions)
class RolePermission(admin.ModelAdmin):
    list_display = ["permission_name", "api_method", "url_identifier", "status",]


admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Student, StudentAdmin)
# admin.site.register(RolePermissions)
admin.site.register(Payment, PaymentsAdmin)
