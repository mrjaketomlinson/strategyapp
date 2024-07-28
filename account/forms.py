# Django
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

# App
from account.models import User, Organization, Team, TeamMember
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
            "created_by",
            "modified_by",
            "organization",
        ]
        widgets = {
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
            "organization": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "name",
            "modified_by",
        ]
        widgets = {
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TeamEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class TeamMemberCreateForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["user", "role", "team"]
        widgets = {"team": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(TeamMemberCreateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["user"].queryset = User.objects.filter(
                organization=self.request.user.organization
            )
        for visible in self.visible_fields():
            add_classes(visible)

        self.fields["user"].label_from_instance = self.user_label_from_instance

    @staticmethod
    def user_label_from_instance(obj):
        return obj.get_full_name()
