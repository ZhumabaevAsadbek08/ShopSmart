from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *
from leads.views import *
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r"user", UserAPIView)

urlpatterns = [
    #Views
    path("admin/", admin.site.urls),
    path("", LandingPageView.as_view(), name="landing-page"),
    #Registration-Views
    path("sign_up", SignUpView, name="sign-up"),
    path("log_in", LogInView, name="log-in"),
    path("log_out", LogoutView.as_view(), name="log-out"),
    #API-Views
    path("api/v1/", include(router.urls), name="api-users"),
    #Bot
    path('webhook/', webhook, name='webhook'),
    #More-URL
    path("", include("leads.detail-urls"), name="details"),
    path("form/", include("leads.form-urls"), name="forms"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)