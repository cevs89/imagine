from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.task_system.models import TasksModels

User = get_user_model()


class APIManageTasksStatusCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="testuser@gmail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.task = TasksModels.objects.create(
            name="Manage Task 1", description="Description 1"
        )
        self.task_status_complete = TasksModels.objects.create(
            name="Manage Task 2", description="Description 2", status="COMPLETE"
        )

    def test_change_same_status_that_tasks_has_error(self):
        data = {"status": "NEW"}
        response = self.client.post(
            f"/v1/manage/task/state/{self.task.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "message_error": f"Current status for tasks {self.task.name} is {self.task.status} the same that you try to update."
            },
        )

    def test_change_not_allowed_value_and_longer_than_8(self):
        data = {"status": "not_allowed"}
        response = self.client.post(
            f"/v1/manage/task/state/{self.task.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"status": ["unallowed value not_allowed", "max length is 8"]},
        )

    def test_change_correct_status_available(self):
        data = {"status": "PROGRESS"}
        response = self.client.post(
            f"/v1/manage/task/state/{self.task.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["message_success"], "Status was updated success"
        )
        self.assertEqual(response.json()["data"]["status"], "PROGRESS")

    def test_try_change_status_in_tasks_does_not_exists(self):
        data = {"status": "REVIEW"}
        response = self.client.post(
            "/v1/manage/task/state/18398451/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"message_error": "Task Doesn't exists"})

    def test_try_change_wrong_method(self):
        data = {"status": "NEW"}
        response = self.client.put(
            f"/v1/manage/task/state/{self.task.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.json(), {"detail": 'Method "PUT" not allowed.'})
