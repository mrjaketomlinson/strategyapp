# Django
from django import forms
# App
from strategy.models import Assumption, BusinessProblem


class AssumptionCreateForm(forms.ModelForm):
    class Meta:
        model = Assumption
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "summary",
            # "description"
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(AssumptionCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


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
            visible.field.widget.attrs['class'] = 'form-control'