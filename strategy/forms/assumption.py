# Django
from django import forms
# App
from strategy.models import Assumption, BusinessProblem
from utils.form_utils import add_classes


class AssumptionCreateForm(forms.ModelForm):
    class Meta:
        model = Assumption
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "business_problem",
            "summary",
            # "description"
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
            "business_problem": forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(AssumptionCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class AssumptionEditForm(forms.ModelForm):
    class Meta:
        model = Assumption
        fields = [
            "modified_by",
            "summary",
            "description"
        ]
        widgets = {
            "modified_by": forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(AssumptionEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)