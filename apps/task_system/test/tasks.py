from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.task_system.models import TasksModels


class TestCaseTasksModels(TestCase):
    def setUp(self):
        try:
            self.queryset = TasksModels.objects.create(
                name="Tarea Uno", description="Esto es una description"
            )
            self.queryset.full_clean()
            self.queryset.save()
        except (AttributeError, ValueError, TypeError):
            self.fail()

    def test_only_with_mandatory_fields(self):

        try:
            queryset = TasksModels.objects.create(
                name="Tarea Dos",
                description="Esto es una description",
            )
            queryset.full_clean()
            queryset.save()
        except ValidationError:
            self.fail()

        else:
            self.assertIsInstance(queryset, TasksModels)
            self.assertEqual(queryset.name, "Tarea Dos")
            self.assertEqual(queryset.description, "Esto es una description")

    def test_with_all_fields_specified(self):
        try:
            queryset = TasksModels.objects.create(
                name="Tarea Dos",
                description="Esto es una description",
                status="COMPLETE",
                is_active=False,
            )
            queryset.full_clean()
            queryset.save()
        except ValidationError:
            self.fail()
        else:
            self.assertIsInstance(queryset, TasksModels)
            self.assertEqual(queryset.name, "Tarea Dos")
            self.assertEqual(queryset.description, "Esto es una description")
            self.assertEqual(queryset.status, "COMPLETE")
            self.assertEqual(queryset.is_active, False)

    def test_with_incorrect_status_enums(self):
        with self.assertRaises(ValidationError):
            queryset = TasksModels.objects.create(
                name="Tarea Dos",
                description="Esto es una description",
                status="NO",
            )
            queryset.full_clean()

    def test_with_lower_status_enums(self):
        with self.assertRaises(ValidationError):
            queryset = TasksModels.objects.create(
                name="Tarea Dos",
                description="Esto es una description",
                status="new",
            )
            queryset.full_clean()

    def test_limited_max_length_status(self):
        with self.assertRaises(ValidationError):
            try:
                with transaction.atomic():
                    TasksModels.objects.create(
                        name="Tarea Dos",
                        description="Esto es una description",
                        status="THIS_CODE_IS_LONG_THAN_PERMIT",
                    )
            except (Exception, IntegrityError) as e:
                raise ValidationError(e) from e

    def test_limited_max_length_in_name(self):
        _name_long = "This name is too long" * 10
        with self.assertRaises(ValidationError):
            try:
                with transaction.atomic():
                    TasksModels.objects.create(
                        name=_name_long,
                        description="Esto es una description",
                    )
            except (Exception, IntegrityError) as e:
                raise ValidationError(e) from e
