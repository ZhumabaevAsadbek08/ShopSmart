from django.urls import path
from .views import *

app_name = "details"

urlpatterns = [
    path("profile/<slug:slug>", ProfileDetailView.as_view(), name="profile"),
]