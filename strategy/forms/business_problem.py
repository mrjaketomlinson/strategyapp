# Django
from django import forms
# App
from strategy.models import BusinessProblem


class BusinessProblemCreateForm(forms.ModelForm):
    class Meta:
        model = BusinessProblem
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "summary",
            "description"
        ]
        widgets = {
            "organization": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(BusinessProblemCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BusinessProblemEditForm(forms.ModelForm):
    class Meta:
        model = BusinessProblem
        fields = [
            "modified_by",
            "summary",
            "description"
        ]
        widgets = {
            "modified_by": forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(BusinessProblemEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'