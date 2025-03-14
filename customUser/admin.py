from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("phone","name", "is_staff", "is_active","is_verified","is_superuser","otp","otp_expiry","otp_max_out","max_otp_try")
    list_filter = ("phone","name", "is_staff", "is_active","is_verified","is_superuser")
    fieldsets = (
        (None, {"fields": ("phone","name", "password","otp","otp_expiry","otp_max_out","max_otp_try")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_verified","is_superuser", "groups", "user_permissions",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone","name", "password1", "password2", "is_staff",
                "is_active","is_verified","is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("phone",)
    ordering = ("phone",)


admin.site.register(CustomUser, CustomUserAdmin)

