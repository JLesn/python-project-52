from django.test import TestCase
from django.urls import reverse
from .models import Status
from django.contrib.auth import get_user_model

User = get_user_model()

class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.login(
            username="testuser",
            password="12345"
        )
        self.status = Status.objects.create(name="In progress")

    def test_status_list_view(self):
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "In progress")

    def test_create_status(self):
        response = self.client.post(
            reverse("status_create"),
            {"name": "Completed"}
        )
        self.assertRedirects(response, reverse("statuses"))
        self.assertTrue(Status.objects.filter(name="Completed").exists())

    def test_update_status(self):
        response = self.client.post(
            reverse("status_update", args=[self.status.id]),
            {"name": "Updated status"}
        )
        self.assertRedirects(response, reverse("statuses"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated status")

    def test_delete_status(self):
        response = self.client.post(reverse("status_delete", args=[self.status.id]))
        self.assertRedirects(response, reverse("statuses"))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

