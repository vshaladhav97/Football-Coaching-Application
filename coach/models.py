from django.db import models
from customer.models import User
from django.db.models import Q
from model_utils import Choices
from customer.managers import QueryManager
# Create your models here.


class Coach(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    town = models.TextField(max_length=1000, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField(upload_to='avatars', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.first_name)



ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'profile_image'),
    ('2', 'first_name'),
    ('3', 'last_name'),
    ('4', 'town'),
    ('5', 'postal_code'),
    ('5', 'address')
)


def query_coachs_by_args(request, **kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column
    queryset = Coach.objects.all()
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


class CoachDocuments(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=False, blank=False)
    file_path = models.FileField(upload_to='coach_documents', blank=True, null=True, max_length=1000)
    actual_filename = models.CharField(max_length=500, null=False, blank=False)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return "{}".format(self.coach)

