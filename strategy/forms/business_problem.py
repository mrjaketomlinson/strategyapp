# Django
from django import forms

# App
from account.models import Team, TimePeriod
from strategy.models import BusinessProblem
from utils.form_utils import add_classes


class BusinessProblemCreateForm(forms.ModelForm):
    class Meta:
        model = BusinessProblem
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "is_public",
            "category",
            "teams",
            "time_period",
            "summary",
            "description",
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(BusinessProblemCreateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["teams"].queryset = Team.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization
            )
        for visible in self.visible_fields():
            add_classes(visible)


class BusinessProblemEditForm(forms.ModelForm):
    class Meta:
        model = BusinessProblem
        fields = [
            "modified_by",
            "is_public",
            "category",
            "teams",
            "time_period",
            "summary",
            "description",
        ]
        widgets = {"modified_by": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(BusinessProblemEditForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["teams"].queryset = Team.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization
            )
        for visible in self.visible_fields():
            add_classes(visible)
