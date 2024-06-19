from django.contrib import admin
from .models import *
from .forms import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.forms.widgets import Media
from django.db import models

class DefaultAdmin(admin.ModelAdmin):
    ordering = ["created_at"]
    date_hierarchy = "created_at"
    list_per_page = 7

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe("<img src='{url}' style='border-radius: 2px;' width='24px' height='24px' />".format(
                url=obj.photo.url, ))

    photo_preview.short_description = f"Фото"

@admin.register(User)
class UserAdmin(DefaultAdmin):
    list_display = ["username", "full_name", "email", "photo_preview", "gender", "birthday", "is_superuser", "is_staff", "is_active", "last_login", "updated_at", "created_at"]
    list_filter = ["birthday", "gender", "is_superuser", "is_staff", "is_active", "updated_at", "created_at"]
    search_fields = ["username", "email"]
    actions = ["make_superuser", "make_staff", "make_active", "ban", "delete"]
    fieldsets = [
        ("Редактровать", {"fields": ["first_name", "last_name", "username", "email", "gender", "birthday"]}),
        ("Допольнительные", {"fields": ["photo", "user_permissions"]}),
    ]

    def full_name(self, obj):
        return obj.full_name()

    def make_superuser(self, request, queryset):
        queryset.update(is_superuser=True)
        queryset.update(is_staff=True)
        queryset.update(is_active=True)

    def make_staff(self, request, queryset):
        queryset.update(is_superuser=False)
        queryset.update(is_staff=True)
        queryset.update(is_active=True)

    def make_active(self, request, queryset):
        queryset.update(is_superuser=False)
        queryset.update(is_staff=False)
        queryset.update(is_active=True)

    def ban(self, request, queryset):
        queryset.update(is_superuser=False)
        queryset.update(is_staff=False)
        queryset.update(is_active=False)

    def delete(self, request, queryset):
        queryset.delete()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    make_superuser.short_description = f"Сделать админом выбранные {User._meta.verbose_name_plural}"
    make_staff.short_description = f"Сделать сотрудником выбранные {User._meta.verbose_name_plural}"
    make_active.short_description = f"Сделать клиентом выбранные {User._meta.verbose_name_plural}"
    delete.short_description = f"Удалить выбранные {User._meta.verbose_name_plural}"
    ban.short_description = f"Забанить выбранные {User._meta.verbose_name_plural}"
    full_name.short_description = f"Имя"

@admin.register(UserProfile)
class UserProfileAdmin(DefaultAdmin):
    list_display = ["user", "updated_at", "created_at"]
    list_filter = [ "updated_at", "created_at"]
    search_fields = ["user__username"]
    actions = ["delete"]

admin.site.unregister(Group)
admin.site.site_title = "Title"
admin.site.site_header = "Админ-панель сайта Title"
admin.site.index_title = "Добро пожаловать в админ-панель"