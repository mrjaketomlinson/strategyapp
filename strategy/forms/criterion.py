# Django
from django import forms
# App
from strategy.models import Criterion
from utils.form_utils import add_classes


class CriterionCreateForm(forms.ModelForm):
    class Meta:
        model = Criterion
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "name",
            "criterion_type"
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(CriterionCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)


class CriterionEditForm(forms.ModelForm):
    class Meta:
        model = Criterion
        fields = [
            "modified_by",
            "name",
            "criterion_type"
        ]
        widgets = {
            "modified_by": forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(CriterionEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            add_classes(visible)
