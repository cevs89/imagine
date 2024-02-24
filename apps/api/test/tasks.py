from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.task_system.models import TasksModels

User = get_user_model()


class APITasksViewModelsCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="testuser@gmail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.task1 = TasksModels.objects.create(
            name="Task 1", description="Description 1"
        )
        self.task2 = TasksModels.objects.create(
            name="Task 2", description="Description 2"
        )
        self.name_long = "This name is too long" * 10

    def test_create_tasks_post_with_mandatory_fields_201_created(self):
        data = {"name": "bar", "description": "description"}
        response = self.client.post("/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["status"], "NEW")

    def test_create_tasks_post_limited_max_length_in_name(self):
        data = {"name": self.name_long, "description": "description"}
        response = self.client.post("/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"name": ["Ensure this field has no more than 150 characters."]},
        )

    def test_create_tasks_post_without_description_and_max_length_in_name(self):
        data = {"name": self.name_long}
        response = self.client.post("/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "name": ["Ensure this field has no more than 150 characters."],
                "description": ["This field is required."],
            },
        )

    def test_create_tasks_post_with_correct_status_value(self):
        data = {"name": "bar", "description": "description", "status": "COMPLETE"}
        response = self.client.post("/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tasks_post_with_incorrect_status_value(self):
        data = {"name": "bar", "description": "description", "status": "incorrect"}
        response = self.client.post("/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"status": ['"incorrect" is not a valid choice.']}
        )

    def test_get_tasks_with_wrong_url(self):
        response = self.client.get("/v1/tasks/44")
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_get_single_tasks_register(self):
        response = self.client.get(f"/v1/tasks/{self.task1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Task 1")
        self.assertEqual(response.json()["description"], "Description 1")

    def test_get_all_tasks_correct_url(self):
        response = self.client.get("/v1/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()) >= 1, "Does not data")

    def test_put_update_tasks_single_register(self):
        data = {"name": "bar", "description": "description", "status": "COMPLETE"}
        response = self.client.put(f"/v1/tasks/{self.task1.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "bar")
        self.assertEqual(response.json()["description"], "description")
        self.assertEqual(response.json()["status"], "COMPLETE")

    def test_delete_tasks_no_found_data(self):
        response = self.client.delete("/v1/tasks/18398451/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
