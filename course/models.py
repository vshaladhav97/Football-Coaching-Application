# from sourcecode.customer.views import customer_view
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import AutoField
from master.models import CourseType, EventType, WeekDay, Location, AgeGroup, ClassStatus, Months, PlayingSurface, Ages
from coach.models import Coach
from customer.models import Student, Role, User, Customer, Payment
from model_utils import Choices
from django.db.models import Q
from customer.managers import QueryManager
import datetime
# Create your models here.


class CourseDetail(models.Model):
    logo = models.ImageField(upload_to='course_logo', null=True, blank=True)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name="course_details")
    no_of_groups = models.IntegerField(null=True, blank=True)
    no_of_weeks = models.IntegerField(null=True, blank=True)
    joining_fee = models.CharField(max_length=250, null=True, blank=True)
    course_description = models.TextField(max_length=1000, null=True, blank=True)
    event_type = models.ForeignKey(EventType, null=True, blank=True, on_delete=models.CASCADE)
    default_duration_in_days = models.IntegerField(default=0)
    default_course_rate = models.CharField(max_length=250, blank=True, null=True)
    execution_duration = models.CharField(max_length=250, blank=True, null=True)
    weekday = models.ForeignKey(WeekDay, null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    single_day = models.CharField(max_length=250, null=True, blank=True)
    two_days = models.CharField(max_length=250, null=True, blank=True)
    three_days = models.CharField(max_length=250, null=True, blank=True)
    four_days = models.CharField(max_length=250, null=True, blank=True)
    five_days = models.CharField(max_length=250, null=True, blank=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    town = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True)
    playing_surface = models.ForeignKey(PlayingSurface, null=True, blank=True, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE)
    class_status = models.ForeignKey(ClassStatus, on_delete=models.CASCADE)
    welcome_message = models.CharField(max_length=500, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()
    def __str__(self):
        return "course_type:{} and  location:{}".format(self.course_type, self.location)


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'course_type'),
    ('2', 'course_description'),
    ('3', 'default_course_rate'),
)


def query_course_by_args(request, **kwargs):
    # check_user_is_superuser = Customer.objects.filter(username=request.user.username).values('is_superuser')
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column
    queryset = CourseDetail.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(course_type__course_name__icontains=search_value) |
                                   Q(start_date__icontains=search_value) |
                                   Q(end_date__icontains=search_value) |
                                   Q(end_date__icontains=search_value) |
                                   Q(course_description__icontains=search_value) |
                                   Q(default_course_rate__icontains=search_value) |
                                   Q(location__location__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

def query_course_by_args_for_booking_list(request, **kwargs):
    # check_user_is_superuser = Customer.objects.filter(username=request.user.username).values('is_superuser')
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column
    queryset = CourseDetail.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(course_type__course_name__icontains=search_value) |
                                   Q(start_date__icontains=search_value) |
                                   Q(end_date__icontains=search_value) |
                                   Q(end_date__icontains=search_value) |
                                   Q(location__location__icontains=search_value) |
                                   Q(default_course_rate__icontains=search_value)                                 
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


# class CourseGroupData(models.Model):
#     course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE, related_name="course_group")
#     age = models.ForeignKey(Ages, null=True, blank=True, on_delete=models.CASCADE)
#     from_drop_off_time = models.TimeField(null=True, blank=True)
#     from_pick_up_time = models.TimeField(null=True, blank=True)
#     to_drop_off_time = models.TimeField(null=True, blank=True)
#     to_pick_up_time = models.TimeField(null=True, blank=True)
#     start_time = models.TimeField(null=True, blank=True)
#     end_time = models.TimeField(null=True, blank=True)
#     maximum_capacity = models.CharField(max_length=250, null=True, blank=True)

# class CourseGroupData(models.Model):
#     course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE,related_name="course_group")
#     age = models.ForeignKey(Ages, null=True, blank=True, on_delete=models.CASCADE)
#     from_drop_off_time = models.TimeField(null=True, blank=True)
#     from_pick_up_time = models.TimeField(null=True, blank=True)
#     to_drop_off_time = models.TimeField(null=True, blank=True)
#     to_pick_up_time = models.TimeField(null=True, blank=True)
#     start_time = models.TimeField(null=True, blank=True)
#     end_time = models.TimeField(null=True, blank=True)
#     maximum_capacity = models.CharField(max_length=250, null=True, blank=True)
#     coach1 = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE, related_name="coach_1")
#     coach2 = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE, related_name="coach_2")

class CourseGroupData(models.Model):
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE, related_name="course_details")
    age = models.ForeignKey(Ages, null=True, blank=True, on_delete=models.CASCADE, related_name="ages")
    from_drop_off_time = models.TimeField(null=True, blank=True)
    from_pick_up_time = models.TimeField(null=True, blank=True)
    to_drop_off_time = models.TimeField(null=True, blank=True)
    to_pick_up_time = models.TimeField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    maximum_capacity = models.CharField(max_length=250, null=True, blank=True)
    coach1 = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE, related_name="coach_1")
    coach2 = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE, related_name="coach_2")

    def __str__(self):
        return "{}".format(self.age)


class CourseLocation(models.Model):
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE, related_name="course_location")
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE)
    total_seats = models.IntegerField(null=True, blank=True)
    available_seats = models.IntegerField()
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()


    def __str__(self):
        return "{}".format(self.location)

class CourseMonths(models.Model):
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    month = models.ForeignKey(Months, null=True, blank=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.month)


class CourseAgeGroup(models.Model):
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, null=True, blank=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.age_group)


class CourseWeekDayMapping(models.Model):
    weekday = models.ForeignKey(WeekDay, null=True, blank=True, on_delete=models.CASCADE)
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.weekday)

class CourseRateMapping(models.Model):
    course_duration = models.CharField(max_length=250, blank=True, null=True)
    custom_course_rate = models.DecimalField(max_digits=5, null=True, blank=True, decimal_places=2)
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()
    
    def __str__(self):
        return "{}".format(self.course_duration)


class CourseScheduleDetail(models.Model):
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    week_number = models.IntegerField(null=True, blank=True)
    day_number = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.week_number)

class BookCourseDetail(models.Model):
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    tokens = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()
    
    def __str__(self):
        return "{}".format(self.course)


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'student'),
    ('2', 'course'),
    ('3', 'location'),
    ('4', 'start_date'),
    ('5', 'end_date'),
)


def query_courses_booked_by_args(request, **kwargs):
    # check_user_is_superuser = Customer.objects.filter(username=request.user.username).values('is_superuser')
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column

    role = str(request.user.role)

    if role == "Customer":
        queryset = BookCourseDetail.objects.filter(student__in=
            Student.objects.filter(
                customer=Customer.objects.get(email=request.user)).values('id'))
    else:
        queryset = BookCourseDetail.objects.all()

    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(course__course_type__course_name__icontains=search_value) |
                                   Q(student__first_name__icontains=search_value) |
                                   Q(location__location__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


class Events(models.Model):
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    course_detail = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, default="scheduled")
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()
    
    def __str__(self):
        return "{}".format(self.event_type)


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'student'),
    ('2', 'course_detail'),
    ('3', 'event_type'),
    ('4', 'start_date'),
    ('5', 'end_date'),
    ('6', 'title'),
)


def query_events_by_args(request, **kwargs):
    # check_user_is_superuser = Customer.objects.filter(username=request.user.username).values('is_superuser')
    draw = int(kwargs.get('draw', None)[0])
    # print(draw)
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column

    date = datetime.datetime.now().date()
    queryset = Events.objects.filter(start_date=date)

    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(course_detail__course_type__course_name__icontains=search_value) |
                                   Q(student__first_name__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


class Notification(models.Model):
    message = models.CharField(max_length=250, null=True, blank=True)
    from_role_id = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE, related_name="from_role_id")
    from_user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="from_user_id")
    to_role_id = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE, related_name="to_role_id")
    to_user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="to_user_id")
    created_date = models.DateField(null=True, blank=True)
    viewed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()
    
    def __str__(self):
        return "{}".format(self.from_user_id)


class UserAttendance(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=250, default="Abs")
    deleted = models.BooleanField(default=False)
    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.user)

class AccountRecordKeeping(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return 'Comment {}'.format(self.comment)


class Cart(models.Model):
    """Let Cart be a meta. And order_items is reverse relation"""
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    objects = QueryManager()

    def __str__(self):
        return "{}".format(self.total)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(CourseLocation, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
    month = models.ForeignKey(Months, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    purchased_qty = models.IntegerField(default=0)
    purchased = models.BooleanField(default=False)
    booked_qty = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    objects = QueryManager()

    def __str__(self):
        return "{}".format(self.location)

class BlockType(models.Model):
    block_color = models.CharField(max_length=255, null=True, blank=True)
    font_color = models.CharField(max_length=255, null=True, blank=True)
    display_text = models.CharField(max_length=255, null=True, blank=True)
    display_character = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.block_color)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


# class ClassRegister(models.Model):
#     course = models.ForeignKey(CourseDetail, null=True, blank=True, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
#     class_date = models.DateField()

class BookingCustomerStudentDetails(models.Model):
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseType, null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.customer)


class PriceMatrix(models.Model):
    version = models.IntegerField()
    course_detail = models.ForeignKey(CourseDetail, on_delete=CASCADE)
    single_day = models.FloatField(default=0)
    two_days = models.FloatField(default=0)
    three_days = models.FloatField(default=0)
    four_days = models.FloatField(default=0)
    five_days = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "{}".format(self.course_detail)

class EventWeek(models.Model):
    event = models.ForeignKey(Events, on_delete=CASCADE)
    week_number = models.IntegerField()
    week_start_date = models.DateField()
    week_end_date = models.DateField()

    def __str__(self):
        return "{}".format(self.id)

class DayWiseWeekDetails(models.Model):
    event_week = models.ForeignKey(EventWeek, on_delete=CASCADE)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    student = models.ForeignKey(Student, on_delete=CASCADE)
    selection_array = models.JSONField()
    number_of_days_pass = models.IntegerField()
    cost = models.FloatField()  

    def __str__(self):
        return "{}".format(self.id)

class NurseryAndWeeklyStudentOrderDetails(models.Model):
    student = models.ForeignKey(Student, on_delete=CASCADE)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}".format(self.student)

class Order(models.Model):
    """order"""
    event_week = models.ManyToManyField(EventWeek, blank=True)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    total_cost = models.FloatField()
    price_matrix = models.ForeignKey(PriceMatrix, on_delete=CASCADE)
    discounted_amount = models.FloatField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}".format(self.event_week)

class OrderSummary(models.Model):
    """order summary"""
    order = models.ForeignKey(Order, on_delete=CASCADE, null=True, related_name="order_summary")
    day_wise_week_details = models.ForeignKey(DayWiseWeekDetails, null=True, blank=True, on_delete=CASCADE)
    nursery_and_weekly_student_order_details = models.ForeignKey(NurseryAndWeeklyStudentOrderDetails, null=True, blank=True, on_delete=CASCADE)
    payment = models.ForeignKey(Payment, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.order)

