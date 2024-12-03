# Django
from django import forms
# App
from account.models import Team, TimePeriod, User
from project.models import Project
from utils.form_utils import add_classes


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "organization",
            "strategy",
            "created_by",
            "modified_by",
            "time_period",
            "owner",
            "working_group",
            "teams",
            "summary",
            "description",
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "strategy": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["teams"].queryset = Team.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization
            )
            users = User.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["owner"].queryset = users
            self.fields["working_group"].queryset = users
        for visible in self.visible_fields():
            add_classes(visible)


class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "modified_by",
            "time_period",
            "owner",
            "working_group",
            "teams",
            "summary",
            "description",
        ]
        widgets = {"modified_by": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ProjectEditForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["teams"].queryset = Team.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization
            )
            users = User.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["owner"].queryset = users
            self.fields["working_group"].queryset = users
        for visible in self.visible_fields():
            add_classes(visible)
