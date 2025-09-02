from django.test import TestCase
from django.urls import reverse
from .models import MyUser

class UserCRUDTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            password="strongpassword123"
        )

    def test_user_creation(self):
        user_count = MyUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("strongpassword123"))

    def test_user_registration_view(self):
        response = self.client.post(reverse("create"), {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MyUser.objects.filter(username="newuser").exists())

    def test_user_update_view(self):
        self.client.login(username="testuser", password="strongpassword123")
        response = self.client.post(reverse("user_update", args=[self.user.id]), {
            "first_name": "Updated",
            "last_name": "User",
            "username": "testuser",
            "new_password1": "",
            "new_password2": ""
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_user_delete_view(self):
        self.client.login(username="testuser", password="strongpassword123")
        response = self.client.post(reverse("user_delete", args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MyUser.objects.filter(username="testuser").exists())

    def test_permission_on_update_other_user(self):
        other_user = MyUser.objects.create_user(
            username="otheruser", password="anotherpassword123"
        )
        self.client.login(username="testuser", password="strongpassword123")
        response = self.client.post(reverse("user_update", args=[other_user.id]), {
            "first_name": "Hack",
            "last_name": "User",
            "username": "hacked"
        })
        self.assertEqual(response.status_code, 302)
        other_user.refresh_from_db()
        self.assertEqual(other_user.first_name, "")