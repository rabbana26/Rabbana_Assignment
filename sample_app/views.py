from django.shortcuts import render

from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import *


# import django_filters
# from . filters import *
# from django_filters.rest_framework import DjangoFilterBackend

# from django_filters import rest_framework

from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction

from datetime import datetime, timezone
from datetime import time
from datetime import date
from .decorators import is_user_authenticated



@csrf_exempt

def login(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, "code": 1, 'error': "f'method {request.method} is not allowed'"})
    user_data = json.loads(request.body)
    print(user_data)
    if User.objects.filter(email=user_data['email']).exists():
        user = User.objects.get(email=user_data['email'])
        userData = user.to_dict()
        
        if user.check_password(user_data['password']):
            return JsonResponse({"success": True, "code": 0, "status": "Login Successfull", "data":{"user": userData, 'access_token':user.token}})
        else:
            return JsonResponse({"success" : False, "code": 1, "status":"Email/password did not match"})    
    else:
        return JsonResponse({"success" : False, "code": 1, "status":"Email does not exist"})

@csrf_exempt
@transaction.atomic
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, "code": 1, 'status': "f'method {request.method} is not allowed'"})
    print("signup in")
    user_data = json.loads(request.body)
    if User.objects.filter(email=user_data['email']).exists():
        print("1")
        return JsonResponse({"success" : False, "code": 1, "status":"Email alreay exists."})
    else:
        try:
            print("2", user_data)
            with transaction.atomic():
                user = User.objects.create_user(user_data["email"], user_data["password"])
                user.name = user_data["name"]
#                user.location = Point(user_data["location"]["longitude"],user_data["location"]["latitude"])
                user.email = user_data["email"]
                user.save()
                userData = user.to_dict()
                

                return JsonResponse({"success": True, "code": 0, "status": "Successfully registered", "data":{"user": userData, "access_token": user.token}})
        except Exception as e:
            print("3")
            print(str(e))
            return JsonResponse({"success": False, "code": 2, "status":str(e)})







# Create your views here.
class ManagerViewSet(viewsets.ModelViewSet):
    #API endpoint for User
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    #API endpoint for User
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filter_class = EmployeFilter

