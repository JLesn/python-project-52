from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task

User = get_user_model()

class TaskCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass12345')
        self.other_user = User.objects.create_user(username='other', password='pass12345')

        self.status = Status.objects.create(name='In progress')

        self.label1 = Label.objects.create(name='backend')
        self.label2 = Label.objects.create(name='urgent')

        self.task = Task.objects.create(
            name='Test task',
            description='Task description',
            status=self.status,
            author=self.user,
            executor=self.other_user,
        )

        self.task.labels.set([self.label1, self.label2])

        self.list_url = reverse('tasks')
        self.create_url = reverse('task_create')
        self.detail_url = reverse('task_detail', args=[self.task.id])
        self.update_url = reverse('task_update', args=[self.task.id])
        self.delete_url = reverse('task_delete', args=[self.task.id])

    def test_create_task(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.post(reverse('task_create'), {
            'name': 'New task',
            'description': 'New task description',
            'status': str(self.status.id),
            'executor': str(self.other_user.id),
            'labels': [str(self.label1.id), str(self.label2.id)],
        })

        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(name='New task')

        self.assertQuerySetEqual(
            new_task.labels.order_by('id').values_list('id', flat=True),
            [self.label1.id, self.label2.id],
            ordered=True
        )

    def test_create_task_requires_auth(self):
        self.client.logout()
        resp = self.client.get(self.create_url)
        self.assertRedirects(resp, reverse("login") + f"?next={self.create_url}")

    def test_task_list_view(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task')

    def test_task_list_requires_auth(self):
        self.client.logout()
        resp = self.client.get(self.list_url)
        self.assertRedirects(resp, reverse("login") + f"?next={self.list_url}")

    def test_task_detail_view(self):
        self.client.login(username='author', password='pass12345')
        resp = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.label1.name)
        self.assertContains(resp, self.label2.name)

    def test_task_detail_requires_auth(self):
        self.client.logout()
        resp = self.client.get(self.detail_url)
        self.assertRedirects(resp, reverse("login") + f"?next={self.detail_url}")

    def test_update_task_by_author(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Modified task',
            'description': 'New description',
            'status': str(self.status.id),
            'executor': str(self.other_user.id),
            'labels': [str(self.label2.id)],
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Modified task')
        self.assertQuerySetEqual(
            self.task.labels.order_by('id').values_list('id', flat=True),
            [self.label2.id],
            ordered=True
        )

    def test_update_task_requires_auth(self):
        self.client.logout()
        resp = self.client.get(self.update_url)
        self.assertRedirects(resp, reverse("login") + f"?next={self.update_url}")

    def test_delete_task_by_author(self):
        self.client.login(username='author', password='pass12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


    def test_delete_task_requires_auth(self):
        self.client.logout()
        resp = self.client.get(self.delete_url)

        self.assertRedirects(
            resp,
            reverse("login") + f"?next={self.delete_url}",
            fetch_redirect_response=False
        )


    def test_delete_task_by_non_author_forbidden(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())