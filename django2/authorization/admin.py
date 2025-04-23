from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


@admin.register(get_user_model())
class CustomUserAdmin(ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.password.startswith("pbkdf2_sha256"):
            obj.password = make_password(obj.password)

        super().save_model(request, obj, form, change)


# admin.site.register(get_user_model(), CustomUserAdmin)
