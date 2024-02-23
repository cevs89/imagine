from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path("authentication/", views.obtain_auth_token, name="user_obtain_token"),
]
