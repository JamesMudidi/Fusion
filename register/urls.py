from django.urls import path
from register.views import CreateAndListRegistrationView

app_name = 'register'

urlpatterns = [
    path('', CreateAndListRegistrationView.as_view(),
         name='create_and_list_property'),
]
