# Django
from django import forms

# App
from strategy.models import PlanningEvent
from utils.form_utils import add_classes


class PlanningEventCreateForm(forms.ModelForm):
    class Meta:
        model = PlanningEvent
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "name",
            "time_period",
            "score_type",
            "score_value_type",
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PlanningEventCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class PlanningEventEditForm(forms.ModelForm):
    class Meta:
        model = PlanningEvent
        fields = [
            "modified_by",
            "name",
            "time_period",
            "score_type",
            "score_value_type",
        ]
        widgets = {
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PlanningEventEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)
