import django_filters as filters
from rest_framework import viewsets, serializers

from employee_manager.models import Department, Employee


# region Department


class DepartmentFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Department
        fields = ('name',)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'address', 'head')


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_class = DepartmentFilters
    ordering = ('-id',)


# endregion Department


# region Employee


class EmployeeFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    department = filters.ModelChoiceFilter(queryset=Department.objects.all())

    class Meta:
        model = Employee
        fields = ('name', 'email', 'department')


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id', 'name', 'email', 'date_joined', 'phone', 'department')


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_class = EmployeeFilters
    ordering = ('-id',)


# endregion Employee
