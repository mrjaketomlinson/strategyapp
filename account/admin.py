# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# App
from account.forms import UserCreationForm, UserChangeForm
from account.models import User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "first_name", "last_name", "is_staff"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password", "is_active"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "timezone"]}),
        ("Permissions", {"fields": ["is_staff"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Register UserAdmin
admin.site.register(User, UserAdmin)
