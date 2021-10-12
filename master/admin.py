from django.contrib import admin
from .models import (Company, Location, AgeGroup, AddressDetail, PlayingSurface,
                     CourseType, EventType, WeekDay, ClassStatus,
                     Months, Ages, CourseWiseSuitableLocation)
# Register your models here.


class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ['course_name']


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']


class WeekDayAdmin(admin.ModelAdmin):
    list_display = ['weekday']


class ClassStatusAdmin(admin.ModelAdmin):
    list_display = ['status_name']


class MonthAdmin(admin.ModelAdmin):
    list_display = ['month']


class AgeAdmin(admin.ModelAdmin):
    list_display = ['age']


class PlayingSurfaceAdmin(admin.ModelAdmin):
    list_display = ['surface']

@admin.register(Location)
class EventWeekAdmin(admin.ModelAdmin):
    """for ui sample individual data to display in list"""
    list_display = ["id","company", "location"]

admin.site.register(AddressDetail)
admin.site.register(Company)
# admin.site.register(Location)
admin.site.register(CourseWiseSuitableLocation)
admin.site.register(AgeGroup)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(ClassStatus, ClassStatusAdmin)
admin.site.register(Months, MonthAdmin)
admin.site.register(Ages, AgeAdmin)
admin.site.register(PlayingSurface, PlayingSurfaceAdmin)
