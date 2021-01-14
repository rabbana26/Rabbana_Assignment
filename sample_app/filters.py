import django_filters
from rest_framework import filters
from . models import *

class EmployeFilter(django_filters.FilterSet):
    class Meta:
        model = Employe
        fields = {
            'e_firstname': ['icontains'],
            
        }


