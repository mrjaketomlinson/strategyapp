# Django
from django import forms

# App
from account.models import Team
from strategy.models import BusinessProblem


class BusinessProblemCreateForm(forms.ModelForm):
    class Meta:
        model = BusinessProblem
        fields = [
            "organization",
            "created_by",
            "modified_by",
            "summary",
            "teams",
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
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class BusinessProblemEditForm(forms.ModelForm):
    class Meta:
        model = BusinessProblem
        fields = ["modified_by", "summary", "teams", "description"]
        widgets = {"modified_by": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(BusinessProblemEditForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["teams"].queryset = Team.objects.filter(
                organization=self.request.user.organization
            )
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
