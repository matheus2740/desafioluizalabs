from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from employee_manager import api

router = routers.DefaultRouter()
router.register(r'departments', api.DepartmentViewSet)
router.register(r'employees', api.EmployeeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
]
