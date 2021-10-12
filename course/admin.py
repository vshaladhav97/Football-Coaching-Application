from django.contrib import admin
from .models import (CourseDetail, CourseWeekDayMapping, CourseRateMapping,
                     CourseScheduleDetail, CourseLocation, CourseAgeGroup, CourseMonths,
                     BookCourseDetail, Events, Notification, UserAttendance, AccountRecordKeeping,
                     Cart, CartItem, CourseGroupData, Message, EventWeek,
                     DayWiseWeekDetails, Order, OrderSummary, PriceMatrix, NurseryAndWeeklyStudentOrderDetails)

# Register your models here.


class CourseLocationAdmin(admin.StackedInline):
    model = CourseLocation
    extra = 0
    min_num = 1
    validate_min = True


class CourseAgeGroupAdmin(admin.StackedInline):
    model = CourseAgeGroup
    extra = 0
    min_num = 1
    validate_min = True


class CourseMonthsAdmin(admin.StackedInline):
    model = CourseMonths
    extra = 0
    min_num = 1
    validate_min = True


class CourseDetailAdmin(admin.ModelAdmin):
    inlines = [CourseLocationAdmin, CourseAgeGroupAdmin, CourseMonthsAdmin]
    list_display = ["id",'course_type', 'course_description', 'location','event_type', 'default_duration_in_days']


class CourseWeekDayMappingAdmin(admin.ModelAdmin):
    list_display = ['weekday', 'course_detail', 'start_time', 'end_time']


class CourseRateMappingAdmin(admin.ModelAdmin):
    list_display = ['course_duration', 'custom_course_rate', 'course_detail']


class CourseScheduleDetailAdmin(admin.ModelAdmin):
    list_display = ['course_detail', 'week_number', 'day_number', 'start_time', 'end_time']


class BookCourseDetailAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'start_date', 'end_date']


@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'end_date', 'title']


admin.site.register(CourseDetail, CourseDetailAdmin)
admin.site.register(CourseWeekDayMapping, CourseWeekDayMappingAdmin)
admin.site.register(CourseRateMapping, CourseRateMappingAdmin)
admin.site.register(CourseScheduleDetail, CourseScheduleDetailAdmin)
admin.site.register(BookCourseDetail, BookCourseDetailAdmin)
admin.site.register(CourseLocation)
# admin.site.register(Events)
admin.site.register(Notification)
admin.site.register(UserAttendance)
admin.site.register(AccountRecordKeeping)
admin.site.register(Cart)
admin.site.register(CartItem)
@admin.register(EventWeek)
class EventWeekAdmin(admin.ModelAdmin):
    """for ui sample individual data to display in list"""
    list_display = ["id", "week_number", "week_start_date", "week_end_date", ]
# admin.site.register(EventWeek)
@admin.register(DayWiseWeekDetails)
class DayWiseWeekDetailsAdmin(admin.ModelAdmin):
    """for ui sample individual data to display in list"""
    list_display = ["id", "event_week", "customer", "student", "cost",]
# admin.site.register(DayWiseWeekDetails)

@admin.register(NurseryAndWeeklyStudentOrderDetails)
class NurseryAndWeeklyStudentOrderDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "customer", "order_date",]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """for ui sample individual data to display in list"""
    list_display = ["id", "customer", "total_cost", "price_matrix", "discounted_amount", ]
# admin.site.register(Order)
@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    """for ui sample individual data to display in list"""
    list_display = ["id", "order", "day_wise_week_details", "nursery_and_weekly_student_order_details", "payment", ]
# admin.site.register(OrderSummary)
admin.site.register(PriceMatrix)

@admin.register(CourseGroupData)
class CourseGroupDataAdmin(admin.ModelAdmin):
    list_display = ["id", "course_detail", "age", "start_time", "end_time", "maximum_capacity", "from_drop_off_time", "from_pick_up_time", "to_drop_off_time", "to_pick_up_time",]
admin.site.register(Message)