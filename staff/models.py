from django.db import models
from customer.models import User
from django.db.models import Q
from model_utils import Choices
from customer.managers import QueryManager
# Create your models here.


class Staff(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    landline = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = QueryManager()

    def delete(self):
        self.deleted = True
        self.save()


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'first_name'),
    ('2', 'last_name'),
    ('3', 'email'),
    ('4', 'mobile')
)


def query_staffs_by_args(request, **kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column
    queryset = Staff.objects.all()
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
