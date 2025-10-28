from django.test import TestCase
from django.urls import reverse
from .models import Status
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task

User = get_user_model()

class TaskCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='author', password='pass12345'
        )
        self.other_user = User.objects.create_user(
            username='other', password='pass12345'
        )

        self.status = Status.objects.create(name='In progress')

        self.task = Task.objects.create(
            name='Test task',
            description='Task description',
            status=self.status,
            author=self.user,
            executor=self.other_user,
            labels='backend,urgent',
        )

    def test_create_task(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.post(reverse('task_create'), {
            'name': 'New task',
            'description': 'New task description',
            'status': self.status.id,
            'executor': self.other_user.id,
            'labels': 'frontend',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New task').exists())

    def test_task_list_view(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task')

    def test_task_detail_view(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.description)

    def test_update_task_by_author(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Modified task',
            'description': 'New description',
            'status': self.status.id,
            'executor': self.other_user.id,
            'labels': 'urgent',
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Modified task')

    def test_delete_task_by_author(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_by_non_author_forbidden(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())