# Django
from django import forms


def add_classes(visible):
    if isinstance(visible.field.widget, forms.widgets.CheckboxInput):
        visible.field.widget.attrs["class"] = "form-check-input"
        visible.field.label_classes = ["form-check-label"]
    elif isinstance(visible.field.widget, forms.widgets.Select):
        visible.field.widget.attrs["class"] = "form-select"
        visible.field.label_classes = []
    elif isinstance(visible.field.widget, forms.widgets.SelectMultiple):
        visible.field.widget.attrs["class"] = "form-select"
        visible.field.label_classes = []
    else:    
        visible.field.widget.attrs["class"] = "form-control"
        visible.field.label_classes = ["form-label"]
