from django.urls import path
from .views import HelloFusionCamper

urlpatterns = [
    path("welcome/", HelloFusionCamper.as_view()),
]