from django.urls import path
from .views import GoogleAuthAPIView


urlpatterns = [
    path("auth/google/", GoogleAuthAPIView.as_view(), name="google-auth"),
]