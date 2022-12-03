from multiprocessing.spawn import import_main_path
from unicodedata import name
from django.urls import path
from .views import LogoutView, RegistrationView,LoginView,UsernameValidate
from django.views.decorators.csrf import csrf_exempt
import asyncio

urlpatterns = [
    path('register/',RegistrationView.as_view(), name = "register"),
    path('login/',LoginView.as_view(), name = "login"),
    path('logout/',LogoutView.as_view(), name = "logout"),
    path('validate-username/', csrf_exempt(UsernameValidate.as_view()), name = 'validate-username'),
]
