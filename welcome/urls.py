from django.urls import path
from .views import HelloFusion

urlpatterns = [
    path("welcome/", HelloFusion.as_view(), name="welcome"),
]