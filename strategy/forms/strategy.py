# Django
from django import forms

# App
from strategy.models import Strategy


class StrategyCreateForm(forms.ModelForm):
    problem = forms.CharField(max_length=255, widget=forms.HiddenInput())

    class Meta:
        model = Strategy
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "summary",
            "description",
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(StrategyCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StrategyEditForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = [
            "modified_by",
            "summary",
            "description",
        ]
        widgets = {
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(StrategyEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
