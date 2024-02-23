from rest_framework.routers import DefaultRouter

from apps.api.views.tasks import TasksViewSet

router = DefaultRouter()
router.register("", TasksViewSet, basename="tasks")
urlpatterns = router.urls
