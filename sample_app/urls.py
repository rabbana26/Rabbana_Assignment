

from django.urls import path, include
from rest_framework import routers
from .views import *
from . import views

router = routers.DefaultRouter()
router.register('manager', ManagerViewSet)
router.register('employee', EmployeeViewSet)

urlpatterns = [
    # path('user/login/',views.login, name='login'),
    # path('user/signup/', views.signup, name='signup'),
    path('api/', include(router.urls)),
    
]