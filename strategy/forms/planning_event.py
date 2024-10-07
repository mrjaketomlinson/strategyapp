# Django
from django import forms

# App
from strategy.models import PlanningEvent, CriterionWeight, BusinessProblemScore
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


class CriterionWeightCreateForm(forms.ModelForm):
    class Meta:
        model = CriterionWeight
        fields = [
            "created_by",
            "modified_by",
            "criterion",
            "planning_event",
            "weight",
        ]
        widgets = {
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
            "planning_event": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CriterionWeightCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class BusinessProblemScoreForm(forms.ModelForm):
    class Meta:
        model = BusinessProblemScore
        fields = ["score"]

    def save(self, commit=True):
        # Custom save to handle formset logic
        instance = super().save(commit=False)
        # Check if the instance is new and set additional fields
        if not instance.pk:
            instance.planning_event_business_problem = self.initial[
                "planning_event_business_problem"
            ]
            instance.criterion_weight = self.initial["criterion_weight"]
        if commit:
            instance.save()
        return instance
