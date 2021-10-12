from django.db import models
from model_utils import Choices
from django.db.models import Q
# from course.models import CourseLocation
from customer.managers import QueryManager
from django.core.validators import RegexValidator
# import course.models
# course_location = course.models.CourseLocation()
# from course.models import CourseLocation
# Create your models here.

post_code_validation_regex = r'^(^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}?$)'


class AddressDetail(models.Model):
    address_line_1 = models.CharField(max_length=1000, blank=True, null=True)
    address_line_2 = models.CharField(max_length=1000, blank=True, null=True)
    address_line_3 = models.CharField(max_length=1000, blank=True, null=True)
    town = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(
        max_length=250, blank=True, null=True, default="UK")
    postal_code = models.CharField(max_length=10, null=False, blank=False, validators=[RegexValidator(
        regex=post_code_validation_regex,
    )])
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.town


class PlayingSurface(models.Model):
    surface = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.surface


class Company(models.Model):
    company_name = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.company_name


class Location(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True,
                                on_delete=models.CASCADE, related_name="location_name")
    location = models.CharField(max_length=250, blank=False, null=False)
    playing_surface = models.ForeignKey(
        PlayingSurface, null=True, blank=True, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=1000, blank=True, null=True)
    address_line_2 = models.CharField(max_length=1000, blank=True, null=True)
    address_line_3 = models.CharField(max_length=1000, blank=True, null=True)
    town = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(
        max_length=250, blank=True, null=True, default="UK")
    postal_code = models.CharField(max_length=10, null=False, blank=False, validators=[RegexValidator(
        regex=post_code_validation_regex,
    )])
    logo = models.ImageField(upload_to='course_logo', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def __str__(self):
        return self.location

    def delete(self):
        self.deleted = True
        self.save()


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'company'),
    ('2', 'location'),
    ('3', 'town'),
    ('4', 'postal_code'),
    ('5', 'address_line_1'),
)


def query_location_by_args(request, **kwargs):
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
    queryset = Location.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(company__company_name__icontains=search_value) |
                                   Q(location__icontains=search_value) |
                                   Q(address_line_1__icontains=search_value) |
                                   Q(town__icontains=search_value) |
                                   Q(coursewisesuitablelocation__course_type__course_name__icontains=search_value) |
                                   Q(postal_code__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


class AgeGroup(models.Model):
    age_group_text = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.age_group_text


class Ages(models.Model):
    age = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)
    # course_location = models.ForeignKey(CourseLocation, on_delete=models.Case)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.age


class CourseType(models.Model):
    course_name = models.CharField(max_length=250, blank=False, null=False)
    course_title = models.CharField(max_length=500)
    course_description = models.TextField(
        max_length=1000, null=True, blank=True)
    ages = models.ManyToManyField(Ages)
    logo = models.FileField(upload_to='course_type_logo/')
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.course_name


class CourseWiseSuitableLocation(models.Model):
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.CASCADE)
    course_type = models.ForeignKey(
        CourseType, null=True, blank=True, on_delete=models.CASCADE)


class EventType(models.Model):
    type_name = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.type_name


class WeekDay(models.Model):
    weekday = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.weekday


class ClassStatus(models.Model):
    status_name = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.status_name


class Months(models.Model):
    month = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.month

