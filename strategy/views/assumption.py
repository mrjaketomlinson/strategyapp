# Django
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

# App
from strategy.apps import StrategyConfig
from strategy.forms import (
    AssumptionCreateForm,
    AssumptionEditForm,
    BusinessProblemCreateForm,
)
from strategy.models import BusinessProblem, Strategy, Assumption


def assumption_create(request, related_obj, obj_id):
    model = apps.get_model("strategy", related_obj)
    model_obj = get_object_or_404(model, pk=obj_id)
    if request.method == "POST":
        try:
            form = AssumptionCreateForm(request.POST)
            if form.is_valid():
                assumption = form.save()
                model_obj.assumption_set.add(assumption)
                is_success = True
                msg = ""
                # messages.success(request, "Assumption created successfully!")
            else:
                is_success = False
                msg = ""
                for err, message in form.errors.items():
                    # messages.error(
                    #     request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                    # )
                    msg += f'Field: {err}. Message: {"; ".join(m for m in message)}'
        except Exception as e:
            # messages.error(request, "There was an issue with these assumptions.")
            is_success = False
            msg = "There was an issue creating this assumption."
            # TODO: proper logging
            print(
                f"assumption_create Exception. user: {request.user}, "
                f"related_obj: {related_obj}. "
                f"obj_id: {obj_id}. ",
                e
            )
        return JsonResponse({"is_success": is_success, "msg": msg})
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user
        }
        form = AssumptionCreateForm(initial=initial)
        url = reverse("strategy:assumption_create", kwargs={"related_obj": related_obj, "obj_id": obj_id})
        data = {
            "form": render_to_string(
                "inline_form.html",
                {
                    "form": form,
                    "url": url,
                    "button": "Save",
                },
                request=request,
            )
        }
        return JsonResponse(data)


@require_GET
def assumption_detail(request, assumption_id):
    assumption = get_object_or_404(Assumption, pk=assumption_id)
    context = {"assumption": assumption}
    return render(request, "strategy/assumption_detail.html", context)


def assumption_edit(request, assumption_id):
    assumption = get_object_or_404(Assumption, pk=assumption_id)
    if request.method == "POST":
        form = AssumptionEditForm(request.POST, instance=assumption)
        if form.is_valid():
            assumption = form.save()
            messages.success(request, "Update successful!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {"modified_by": request.user}
        form = AssumptionEditForm(instance=assumption, initial=initial)
        context = {
            "form": form,
            "form_id": "assumption_edit_form",
            "url": reverse(
                "strategy:assumption_edit", kwargs={"assumption_id": assumption.pk}
            ),
            "button": "Update",
        }
        return render(request, "strategy/assumption_edit.html", context)


@require_POST
def assumption_delete(request, assumption_id):
    try:
        assumption = get_object_or_404(
            Assumption, pk=assumption_id, organization=request.user.organization
        )
        assumption.delete()
        messages.success(request, "Business problem deleted successfully.")
    except Exception as e:
        messages.error(request, "There was an issue deleting that business problem.")
        # TODO: proper logging
        print(
            f"assumption_delete Exception. user: {request.user}, assumption: {assumption_id}.",
            e,
        )
    return redirect("strategy:assumption_all")
