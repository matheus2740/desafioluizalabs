from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from employee_manager.managers import EmployeeManager


class Department(models.Model):
    """
        Defines a Department of LuizaLabs.
        Employees work in a Department, and a Department have an optional head
        (Employee in charge of the Department, the de-facto person to contact)
    """

    # NOTE:
    # TextField and CharField are the same thing in PostgreSQL, but they may have significantly different
    # performance and implementation in other RDBMS, such as MySQL, where TextFields are more expensive.
    # The choice of using TextField is based on the assumption that there aren't going to be enough departments
    # to make its cost in some RDBMS significant to the application.
    # If the application is to based on such RDBMS, and the number of departments is large ( > ~10k),
    # then these properties should be re-assessed.

    name = models.CharField("Name", max_length=64)
    description = models.TextField("Description")

    # Some departments may be in different buildings/locations.
    address = models.TextField("Address", null=True)

    # The person responsible for this department, the go-to contact. Not required.
    head = models.ForeignKey(
        'employee_manager.Employee',
        verbose_name='Head of department',
        on_delete=models.PROTECT,
        null=True,
        related_name='heading_department'
    )

    def __str__(self):

        return self.name


class Employee(AbstractBaseUser, PermissionsMixin):
    """
        Defines a LuizaLabs Employee, based on Django's default AbstractBaseUser,
        thus allowing Employees to log into employee_manager.
    """
    # NOTE:
    # Employees must have the is_staff attribute set to true to be able to log into employee_manager.
    # This is based on the assumption that not every employee should be able to access the database of other employees.
    # In a real world use case, inheriting from AbstractUser is probably not desirable, and integration with a proper
    # authentication micro-service / application should be made.
    # For the purposes of this challenge I chose to go the AbstractBaseUser route, and to use JWT for API auth.

    name = models.CharField(verbose_name='Name', max_length=128)
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)
    phone = models.CharField(verbose_name='Telephone Number', max_length=64, null=True)

    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'department_id']