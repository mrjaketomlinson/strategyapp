# Django
from django import forms

# App
from account.models import TimePeriod, User, Team
from strategy.models import (
    PlanningEvent,
    CriterionWeight,
    BusinessProblemScore,
    PlanningEventBusinessProblem,
    BusinessProblem,
    Criterion,
)
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
            "scoring_user",
            "scoring_team",
            "score_value_type",
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(PlanningEventCreateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization,
            )
            self.fields["scoring_user"].queryset = User.objects.filter(
                organization=self.request.user.organization
            )
            self.fields["scoring_team"].queryset = Team.objects.filter(
                organization=self.request.user.organization
            )
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
        self.request = kwargs.pop("request", None)
        super(PlanningEventEditForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["time_period"].queryset = TimePeriod.objects.filter(
                organization=self.request.user.organization,
            )
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
        self.request = kwargs.pop("request", None)
        self.planning_event_id = kwargs.pop("planning_event_id", None)
        super(CriterionWeightCreateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["criterion"].queryset = Criterion.objects.filter(
                organization=self.request.user.organization,
            ).exclude(criterionweight__planning_event_id=self.planning_event_id)
        for visible in self.visible_fields():
            add_classes(visible)


class CriterionWeightEditForm(forms.ModelForm):
    class Meta:
        model = CriterionWeight
        fields = [
            "modified_by",
            "weight",
        ]
        widgets = {
            "modified_by": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CriterionWeightEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class PlanningEventBusinessProblemAssociateForm(forms.ModelForm):
    class Meta:
        model = PlanningEventBusinessProblem
        fields = [
            "planning_event",
            "business_problem",
        ]
        widgets = {
            "planning_event": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.business_problem_ids = kwargs.pop("business_problem_ids", [])
        super(PlanningEventBusinessProblemAssociateForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["business_problem"].queryset = BusinessProblem.objects.filter(
                organization=self.request.user.organization,
            ).exclude(
                planningeventbusinessproblem__business_problem_id__in=self.business_problem_ids
            )
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
