from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

User = get_user_model()

class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass12345"
        )

        self.label = Label.objects.create(name="Urgent")

        self.client.login(username="testuser", password="pass12345")

    def test_create_label(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label'
        })

        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name="New Label").exists())

    def test_create_label_requires_auth(self):
        self.client.logout()

        create_url = reverse('label_create')
        response = self.client.get(create_url)

        expected_url = reverse('login') + f'?next={create_url}'
        self.assertRedirects(response, expected_url)


    def test_labels_list(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Urgent")


    def test_update_label(self):
        response = self.client.post(reverse('label_update', args=[self.label.id]), {
            "name": "Updated Label"
        })

        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")

    def test_update_label_requires_auth(self):
        self.client.logout()

        update_url = reverse('label_update', args=[self.label.id])
        response = self.client.get(update_url)

        expected_url = reverse('login') + f'?next={update_url}'
        self.assertRedirects(response, expected_url)



    def test_delete_label(self):
        response = self.client.post(reverse('label_delete', args=[self.label.id]))

        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_delete_label_in_use_forbidden(self):
        status = Status.objects.create(name="New")
        task = Task.objects.create(
            name="Test task",
            status=status,
            author=self.user
        )
        task.labels.add(self.label)

        response = self.client.post(reverse('label_delete', args=[self.label.id]))

        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())

    def test_delete_label_requires_auth(self):
        self.client.logout()

        delete_url = reverse('label_delete', args=[self.label.id])
        response = self.client.get(delete_url)

        expected_url = reverse('login') + f'?next={delete_url}'
        self.assertRedirects(response, expected_url)