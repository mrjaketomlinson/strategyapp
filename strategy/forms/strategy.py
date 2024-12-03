# Django
from django import forms

# App
from account.models import TimePeriod, User
from strategy.models import Strategy
from utils.form_utils import add_classes


class StrategyCreateForm(forms.ModelForm):
    problem = forms.CharField(max_length=255, widget=forms.HiddenInput())

    class Meta:
        model = Strategy
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "time_period",
            "owner",
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
        super(StrategyCreateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["owner"].queryset = User.objects.filter(
                organization=self.request.user.organization
            )
        for visible in self.visible_fields():
            add_classes(visible)


class StrategyEditForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = [
            "modified_by",
            "time_period",
            "owner",
            "summary",
            "description",
        ]
        widgets = {
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(StrategyEditForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["owner"].queryset = User.objects.filter(
                organization=self.request.user.organization
            )
        for visible in self.visible_fields():
            add_classes(visible)
