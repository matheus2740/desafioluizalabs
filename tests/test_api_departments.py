from django.urls import reverse
from mock import MagicMock
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from employee_manager.models import Department, Employee


class DepartmentTests(APITransactionTestCase):

    def setUp(self):
        user = MagicMock()
        user.is_authenticated.return_value = True
        self.client.force_authenticate(user)

    def tearDown(self):

        Employee.objects.all().delete()
        Department.objects.all().delete()

    def test_create_department(self):
        url = '/api/departments/'
        data = {
            'name': 'Department of Silly Walks',
            'description': 'Department responsible for silly walks'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().name, data['name'])
        self.assertEqual(Department.objects.get().description, data['description'])

    def test_create_department_incomplete(self):
        url = '/api/departments/'
        data = {
            'name': 'Department of Silly Walks',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_departments(self):
        from employee_manager.fixture_util import create_departments

        create_departments(10)

        url = '/api/departments/'
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)

        for item in response.json():

            self.assert_(isinstance(item['id'], int))
            self.assert_(isinstance(item['name'], str))
            self.assert_(len(item['name']) > 0)
            self.assert_(isinstance(item['description'], str))
            self.assert_(len(item['description']) > 0)
            self.assert_(item['address'] is None)
            self.assert_(item['head'] is None)

    def test_update_department(self):

        d = Department.objects.create(name='xxx', description='yyy')

        url = f'/api/departments/{d.id}/'
        data = {
            'name': 'xxx',
            'description': 'zzz'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'xxx')
        self.assertEqual(response.json()['description'], 'zzz')
        self.assertIsNone(response.json()['address'])
        self.assertIsNone(response.json()['head'])

    def test_partial_update_department(self):

        d = Department.objects.create(name='xxx', description='yyy')

        url = f'/api/departments/{d.id}/'
        data = {
            'description': 'zzz'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'xxx')
        self.assertEqual(response.json()['description'], 'zzz')
        self.assertIsNone(response.json()['address'])
        self.assertIsNone(response.json()['head'])

    def test_delete_department(self):

        d = Department.objects.create(name='xxx', description='yyy')

        url = f'/api/departments/{d.id}/'
        data = {}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Department.DoesNotExist):
            dd = Department.objects.get(id=d.id)


