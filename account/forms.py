# Django
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError

# App
from account.models import User, Organization, Team
from utils.form_utils import add_classes


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = (
            "Your password cannot be entirely numeric, related to your "
            "personal info, or a commonly used password. It must be at "
            "least 8 characters in length."
        )
        for visible in self.visible_fields():
            add_classes(visible)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "timezone",
            "is_active",
            "is_staff",
        ]


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class OrganizationCreateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "domain"]

    def __init__(self, *args, **kwargs):
        super(OrganizationCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "name",
            "members",
            "organization",
        ]
        widgets = {
            "organization": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)
