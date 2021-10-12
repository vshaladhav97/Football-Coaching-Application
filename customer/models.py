from __future__ import unicode_literals
from django.db import models
from django.db.models.deletion import CASCADE
from master.models import AddressDetail, AgeGroup, Ages
# from course.models import Events
from model_utils import Choices
# from course.models import CourseDetail
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from json import dumps
from .managers import UserManager, QueryManager
import datetime
from django.core.validators import RegexValidator

# Create your models here.

post_code_validation_regex = r'^(^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}?$)'


class RolePermissions(models.Model):
    permission_name = models.CharField(max_length=100)
    api_method = models.CharField(max_length=100)
    url_identifier = models.CharField(max_length=100)
    status = models.BooleanField(null=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "3.Permissions"

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return 'Permission name: {}, API method: {}'.format(self.permission_name, self.api_method)


class Role(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    role_status = models.BooleanField(null=False)
    permissions = models.ManyToManyField(RolePermissions)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "2. Roles"

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.name


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    deleted = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def delete(self):
        self.deleted = True
        self.save()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return dumps(data)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


def query_super_users_by_args(request, **kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column
    queryset = User.objects.filter(
        role=Role.objects.get(name__iexact="Super User"))
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(first_name__icontains=search_value) |
                                   Q(last_name__icontains=search_value) |
                                   Q(email__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


class Customer(models.Model):
    user = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(
        max_length=255, null=False, blank=False, unique=True)
    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    town = models.TextField(max_length=1000, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True, validators=[RegexValidator(
        regex=post_code_validation_regex,
    )])
    country_code = models.CharField(max_length=3, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='avatars', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return '{}. {} {}'.format(self.id, self.first_name, self.last_name)


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'profile_image'),
    ('2', 'first_name'),
    ('3', 'last_name'),
    ('4', 'email'),
    ('5', 'mobile')
)


def query_users_by_args(request, **kwargs):
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
    queryset = Customer.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(first_name__icontains=search_value) |
                                   Q(last_name__icontains=search_value) |
                                   Q(email__icontains=search_value) |
                                   Q(mobile__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
    )
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    age = models.CharField(max_length=255, null=True, blank=True)
    school_name = models.CharField(max_length=255, null=True, blank=True)
    address_details = models.ForeignKey(
        AddressDetail, null=True, blank=True, on_delete=models.CASCADE)
    age_group = models.ForeignKey(
        AgeGroup, null=True, blank=True, on_delete=models.CASCADE)
    ages = models.ForeignKey(
        Ages, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, null=False, blank=False, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    birthdate = models.DateField(
        null=False, blank=False, default=datetime.date.today)
    medical_issue = models.CharField(max_length=255, null=True, blank=True)
    # select_days_of_week = models.ManyToManyField(DaysOfWeeks)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.first_name


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'first_name'),
    ('2', 'last_name'),
    ('3', 'age'),
    ('4', 'school_name')
)


def query_students_by_args(request, **kwargs):
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
        queryset = Student.objects.filter(
            customer=Customer.objects.get(email=request.user))
    else:
        queryset = Student.objects.all()

    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                   Q(first_name__icontains=search_value) |
                                   Q(last_name__icontains=search_value) |
                                   Q(school_name__icontains=search_value)
                                   )

    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


class CustomerDocuments(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=False, blank=False)
    file_path = models.FileField(
        upload_to='customer_documents', blank=True, null=True, max_length=1000)
    actual_filename = models.CharField(max_length=500, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    # def __str__(self):
    #     self.actual_filename


# class EventWeek()

# class EventWeek(models.Model):
#     event_id = models.ForeignKey(Events, on_delete=models.CASCADE)

# class


PAYMENT_STATUS_COLUMN_CHOICES = Choices(
    ('SENT_TO_PG', 'SENT_TO_PG'),
    ('OK', 'PAID'),
    ('ABORT', 'ABORT'),
    ('FAILED', 'FAILED'),
)


class Payment(models.Model):
    payment_id = models.CharField(max_length=250, unique=True)
    amount = models.FloatField(default=0)
    discount_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    currency = models.CharField(max_length=5, default='GBP')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_COLUMN_CHOICES,
        null=True, blank=True
    )
    description = models.TextField(max_length=1000)
    Payment_gateway_reference_id = models.CharField(
        max_length=250, null=True, blank=True)
    Payment_gateway_response_text = models.TextField(
        max_length=1000, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.status)
