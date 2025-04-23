from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password


@admin.register(get_user_model())
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_editable = ('role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ("username", "first_name", "last_name", "email")
    # ordering = ("username", "email")
    list_display_links = ('username', 'email')

    actions = ()

    def save_model(self, request, obj, form, change):
        if not obj.password.startswith("pbkdf2_sha256"):
            obj.password = make_password(obj.password)

        super().save_model(request, obj, form, change)


# admin.site.register(get_user_model(), CustomUserAdmin)
