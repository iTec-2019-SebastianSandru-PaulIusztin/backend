from django.contrib import admin

from apps.authentication.utils import get_auth_model_class


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_superuser", "is_staff")
    search_fields = ("email",)


admin.site.register(get_auth_model_class(), UserAdmin)
