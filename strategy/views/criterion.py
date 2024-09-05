# Django
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from strategy.forms import CriterionCreateForm, CriterionEditForm
from strategy.models import Criterion


@logged_in_user
@require_GET
def criterion_all(request):
    criteria = Criterion.objects.filter(
        organization=request.user.organization
    ).order_by("name")
    context = {
        "criteria": criteria,
        "breadcrumbs": [
            {"title": "Admin", "url": reverse("account:admin")},
            {"title": "Criteria", "url": reverse("strategy:criterion_all")},
        ],
    }
    return render(request, "strategy/criterion_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def criterion_create(request):
    if request.method == "POST":
        form = CriterionCreateForm(request.POST)
        if form.is_valid():
            criterion = form.save()
            messages.success(request, "Criterion created successfully!")
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
        return redirect("strategy:criterion_all")
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
        }
        form = CriterionCreateForm(initial=initial)
        context = {
            "body": render_to_string(
                "base_form.html",
                {
                    "form": form,
                    "url": reverse("strategy:criterion_create"),
                    "form_id": "criterion-create-form",
                    "button": "Create",
                },
                request=request,
            ),
            "title": "Create new criterion",
        }
        return JsonResponse(context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def criterion_edit(request, criterion_id):
    criterion = get_object_or_404(
        Criterion, pk=criterion_id, organization=request.user.organization
    )
    if request.method == "POST":
        form = CriterionEditForm(request.POST, instance=criterion)
        if form.is_valid():
            criterion = form.save()
            messages.success(request, "Update successful!")
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
        return redirect("strategy:criterion_all")
    else:
        initial = {"modified_by": request.user}
        form = CriterionEditForm(instance=criterion, initial=initial)
        context = {
            "body": render_to_string(
                "base_form.html",
                {
                    "form": form,
                    "url": reverse("strategy:criterion_edit", kwargs={"criterion_id": criterion_id}),
                    "form_id": "criterion-edit-form",
                    "button": "Update",
                },
                request=request,
            ),
            "title": "Update criterion",
        }
        return JsonResponse(context)
