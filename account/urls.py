from django.urls import path
from account.views import RegistrationAPIView, LoginAPIView, LogoutView

app_name = 'account'

urlpatterns = [
    path("register/", RegistrationAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogoutView.as_view()),
]