from django.db import models
from django.contrib.auth.models import *
from django.db.models.signals import *
from django.utils import timezone
from randomslugfield import RandomSlugField
from .validators import *
from django.contrib.humanize.templatetags.humanize import naturaltime
from root import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from datetime import datetime
from django.db.models.signals import m2m_changed
from django.dispatch import Signal, receiver
from decimal import Decimal
from PIL import Image
from random import choice
from django.urls import reverse

#Choices
GENDER_CHOICES = (
    ("MALE", "Мужчина"),
    ("FEMALE", "Женщина"),
    ("OTHER", "Другое"),
)

def user_photo_path(instance, filename):
    return os.path.join("static/storage/user/photos/", datetime.now().date().strftime("%Y/%m/%d"), filename)

class User(AbstractUser):
    date_joined = None
    email = models.EmailField("Адрес электронной почты", max_length=150, unique=True, blank=False, null=True)
    photo = models.ImageField("Фото", upload_to=user_photo_path, blank=True, null=True)
    birthday = models.DateField("День рождения", blank=False, null=True)
    gender = models.CharField("Пол", max_length=150, choices=GENDER_CHOICES, blank=False, null=True)
    is_superuser = models.BooleanField("Админ", default=False, editable=False, blank=False, null=False)
    is_staff = models.BooleanField("Сотрудник", default=False, editable=False, blank=False, null=False)
    is_active = models.BooleanField("Клиент", default=True, editable=False, blank=False, null=False)
    # More
    url = RandomSlugField(length=15, unique=True, editable=False, null=True, blank=True)
    updated_at = models.DateTimeField("Последняя изменения", auto_now=True, editable=False, blank=False, null=True)
    created_at = models.DateTimeField("Создания", auto_now_add=True, editable=False, blank=False, null=True)

    def is_online(self):
        if self.updated_at:
            return (timezone.now() - self.updated_at) < timezone.timedelta(minutes=15)
        return False

    def online_info(self):
        if self.is_online():
            return ("Онлайн")
        if self.updated_at:
            return ("{}").format(naturaltime(self.updated_at))
        return ("Нейзвестно")

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        self.username = self.username.lower()
        return super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="user")
    # More
    updated_at = models.DateTimeField("Последняя изменения", auto_now=True, editable=False, blank=False, null=True)
    created_at = models.DateTimeField("Создания", auto_now_add=True, editable=False, blank=False, null=True)

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователя"

@receiver(post_save, sender=User)
def user_signals(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)