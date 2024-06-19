from django.shortcuts import render
from django.views.generic import *
from django.shortcuts import *
from rest_framework import *
from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework import *
from .models import *
from .forms import *
from .serializers import *
from django.urls import *
from django.contrib.auth.views import *
from django.views.generic.detail import *
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .management.commands.bot import bot
import json
import random

class DefaultView(LoginRequiredMixin):
    login_url = '/log_in'
    page = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page] = True
        context["page"] = self.page

        return context

#Views
class LandingPageView(DefaultView, ListView):
    model = User
    context_object_name = "objects"
    template_name = "leads/landing-page.html"
    page = "landing_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

#Detail-Views
class ProfileDetailView(DefaultView, DetailView):
    model = User
    slug_field = "url"
    context_object_name = "profile"
    template_name = "details/profile.html"
    page = "profile_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

#Registration-Views
def SignUpView(request):
    if not request.user.is_authenticated:
        registration_page = True
        data = {
            "registration_page": registration_page,
            "sign_up_page": registration_page,
            "page": "registration_page",
            "page_2": "sign_up_page",
        }
        return render(request, "registration/sign-up.html", data)
    else:
        return redirect("landing-page")

def LogInView(request):
    if not request.user.is_authenticated:
        registration_page = True
        user = User.objects.get(username="asadbek")
        login(request, user)
        data = {
            "registration_page": registration_page,
            "log_in_page": registration_page,
            "page": "registration_page",
            "page_2": "log_in_page",
        }
        return render(request, "registration/log-in.html", data)
    else:
        return redirect("landing-page")

#API-Views
class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Form-Views
def CreateProfileFormView(request):
    if request.method == "POST":
        profile = User()
        profile.username = request.POST.get("username")
        profile.save()
        data = {
        }
        return JsonResponse(data, safe=False)
    return redirect("landing-page")

#Bot
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'invalid method'})