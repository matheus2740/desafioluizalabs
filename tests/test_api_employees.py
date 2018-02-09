from django.urls import reverse
from mock import MagicMock
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from employee_manager.models import Department, Employee


class EmployeeTests(APITransactionTestCase):

    def setUp(self):
        user = MagicMock()
        user.is_authenticated.return_value = True
        self.client.force_authenticate(user)

    def tearDown(self):

        Employee.objects.all().delete()
        Department.objects.all().delete()

    def test_create_employee(self):
        d = Department.objects.create(name='xxx', description='yyy')

        url = '/api/employees/'
        data = {
            'name': 'Rick Sanchez',
            'email': 'rick.sanchez@fakecompany.com',
            'phone': '(11) 1234-1234',
            'department': str(d.id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, data['name'])
        self.assertEqual(Employee.objects.get().email, data['email'])
        self.assertEqual(Employee.objects.get().phone, data['phone'])
        self.assertEqual(Employee.objects.get().department.id, d.id)

    def test_create_employee_incomplete(self):
        url = '/api/employees/'
        data = {
            'name': 'Rick Sanchez',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_employees(self):
        d = Department.objects.create(name='xxx', description='yyy')

        from employee_manager.fixture_util import create_employees

        create_employees(100)

        url = '/api/employees/'
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 100)

        for item in response.json():

            self.assert_(isinstance(item['id'], int))
            self.assert_(isinstance(item['name'], str))
            self.assert_(len(item['name']) > 0)
            self.assert_(isinstance(item['email'], str))
            self.assert_(len(item['email']) > 0)
            self.assert_(isinstance(item['date_joined'], str))
            self.assert_(len(item['date_joined']) > 0)
            self.assert_(isinstance(item['phone'], str))
            self.assert_(len(item['phone']) > 0)
            self.assert_(isinstance(item['department'], int))

            Department.objects.get(id=item['department'])

    def test_update_employee(self):
        d = Department.objects.create(name='xxx', description='yyy')

        e = Employee.objects.create(**{
            'name': 'Rick Sanchez',
            'email': 'rick.sanchez@fakecompany.com',
            'phone': '(11) 1234-1234',
            'department': d
        })

        url = f'/api/employees/{e.id}/'
        data = {
            'name': 'Morty Sanchez',
            'email': 'morty.sanchez@fakecompany.com',
            'phone': '(11) 1234-1234',
            'department': str(d.id)
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], data['name'])
        self.assertEqual(response.json()['email'], data['email'])
        self.assertEqual(response.json()['phone'], data['phone'])
        self.assertEqual(response.json()['department'], d.id)

    def test_partial_update_employee(self):
        d = Department.objects.create(name='xxx', description='yyy')

        e = Employee.objects.create(**{
            'name': 'Rick Sanchez',
            'email': 'rick.sanchez@fakecompany.com',
            'phone': '(11) 1234-1234',
            'department': d
        })

        url = f'/api/employees/{e.id}/'
        data = {
            'name': 'Morty Sanchez',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], data['name'])
        self.assertEqual(response.json()['email'], 'rick.sanchez@fakecompany.com')
        self.assertEqual(response.json()['phone'], '(11) 1234-1234')
        self.assertEqual(response.json()['department'], d.id)

    def test_delete_employee(self):
        d = Department.objects.create(name='xxx', description='yyy')
        e = Employee.objects.create(**{
            'name': 'Rick Sanchez',
            'email': 'rick.sanchez@fakecompany.com',
            'phone': '(11) 1234-1234',
            'department': d
        })

        url = f'/api/employees/{e.id}/'
        data = {}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Employee.DoesNotExist):
            ee = Employee.objects.get(id=e.id)


