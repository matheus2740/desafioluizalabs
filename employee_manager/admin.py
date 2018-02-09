from django.contrib import admin

from employee_manager.models import Employee, Department


class EmployeeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'email', 'department', 'phone')
    list_filter = ('department',)
    search_fields = ('name', 'email')
    list_display_links = ('name',)


class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description', 'head')
    search_fields = ('name', 'description', 'head__name', 'head__email')
    list_display_links = ('name',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
