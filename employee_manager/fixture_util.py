import random
import names

from employee_manager.models import Department, Employee


ADJECTIVES = {
    'Happy',
    'Sad',
    'Silly',
    'Red',
    'Yellow',
    'Green',
    'Square',
    'Avant-Garde',
    'Relative',
    'Absolute',
    'Funny',
    'Fast'
}

SUBSTANTIVES = {
    'Apples',
    'Technologies',
    'Sophistries',
    'Sciences',
    'Gyms',
    'Offices',
    'Boomerangs',
    'Frameworks',
    'Aliens',
    'Chairs',
    'Arms',
    'Puddings'
}


def create_departments(amount):
    for i in range(amount):
        adjective = random.sample(ADJECTIVES, 1)[0]
        substantive = random.sample(SUBSTANTIVES, 1)[0]
        Department.objects.create(
            name=f'Department of {adjective} {substantive}',
            description=f'This is the department in charge of {substantive} which are {adjective}.'
        )


def create_employees(amount):
    departments = list(Department.objects.all())

    for i in range(amount):
        name = names.get_full_name()
        dotted_name = name.lower().replace(' ', '.')
        Employee.objects.create(
            name=name,
            email=f'{dotted_name}@fakecompany.com',
            phone='({ddd}) {part1}-{part2}'.format(
                ddd=random.randint(10, 99),
                part1=random.randint(1000, 9999),
                part2=random.randint(1000, 9999)
            ),
            department=random.sample(departments, 1)[0]
        )


def create_admin():
    Employee.objects.create_superuser('admin@admin.com', 'testing12345', department=Department.objects.all().first(), is_staff=True)


def associate_heads():
    departments = Department.objects.filter(head__isnull=True)
    employees = list(Employee.objects.all())

    for dept in departments:
        dept.head = random.sample(employees, 1)[0]
        dept.save()
