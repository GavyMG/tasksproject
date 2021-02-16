import json
from django.contrib.auth.models import User
from django.urls import reverse
from tasksapp.models import Task
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TaskViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='testpass')
        self.task1 = Task.objects.create(
            name='Task 1', description='Task description', completed=True, owner_id=self.user)
        self.user2 = User.objects.create(username='test_user_2', password='testpass')
        self.task2 = Task.objects.create(
            name='Task 1', description='Task description', completed=True, owner_id=self.user2)

    def test_task_list_unauthenticated(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content).get('results')), 1)

    def test_task_detail_retrive_by_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.task1.name)

    def test_task_detail_retrive_by_nonowner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_partial_update_by_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('task-detail', kwargs={'pk': self.task1.id}), {'completed': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['completed'])

    def test_task_update_by_owner(self):
        self.client.force_authenticate(user=self.user)
        values = {'name': 'Task 1 Updated', 'description': 'new description for task 1', 'completed': False}
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task1.id}), values)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed'], values.get('completed'))
        self.assertEqual(response.data['description'], values.get('description'))
        self.assertEqual(response.data['name'], values.get('name'))

    def test_task_partial_update_by_nonowner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(reverse('task-detail', kwargs={'pk': self.task1.id}), {'completed': False})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_search(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/tasks/?search=description')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content).get('results')), 1)

    def test_task_create(self):
        self.client.force_authenticate(user=self.user)
        values = {'name': 'Task 2', 'description': 'task 2 created', 'completed': False}
        response = self.client.post(reverse('task-list'), values)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
