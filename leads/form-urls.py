from django.urls import path
from .views import *

app_name = "forms"

urlpatterns = [
    path("profile/create", CreateProfileFormView, name="create-profile"),
]