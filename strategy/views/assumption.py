# Django
from django.apps import apps
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from strategy.forms import AssumptionCreateForm
from strategy.models import Assumption, BusinessProblem


@logged_in_user
@require_http_methods(["GET", "POST"])
def assumption_create(request, business_problem_id):
    try:
        pk = None
        action = ""
        msg = ""
        is_success = False
        business_problem = BusinessProblem.objects.get(
            pk=business_problem_id, organization=request.user.organization
        )
    except BusinessProblem.DoesNotExist:
        msg = "Something went wrong trying to create that assumption with this specific business problem."
        # TODO: Proper error messaging
        print(
            f"assumption_create raised an exception. Business Problem doesn't exist. User: {request.user.pk}. business_problem_id: {business_problem_id}."
        )
        json_response = {
            "is_success": is_success,
            "msg": msg,
            "pk": pk,
            "action": action,
        }
        return JsonResponse(json_response)
    if request.method == "POST":
        try:
            form = AssumptionCreateForm(request.POST)
            if form.is_valid():
                assumption = form.save()
                is_success = True
                pk = assumption.pk
                action = reverse(
                    "strategy:assumption_delete",
                    kwargs={
                        "assumption_id": pk,
                    },
                )
                # messages.success(request, "Assumption created successfully!")
            else:
                is_success = False
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
                f"business_problem_id: {business_problem_id}.",
                e,
            )
        json_response = {
            "is_success": is_success,
            "msg": msg,
            "pk": pk,
            "action": action,
        }
        return JsonResponse(json_response)
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
            "business_problem": business_problem,
        }
        form = AssumptionCreateForm(initial=initial)
        url = reverse(
            "strategy:assumption_create",
            kwargs={"business_problem_id": business_problem_id},
        )
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


@logged_in_user
@require_POST
def assumption_remove_relationship(request, assumption_id, related_obj, obj_id):
    try:
        model = apps.get_model("strategy", related_obj)
        model_obj = get_object_or_404(
            model, pk=obj_id, organization=request.user.organization
        )
        assumption = get_object_or_404(
            Assumption, pk=assumption_id, organization=request.user.organization
        )
        model_obj.assumption_set.remove(assumption)
        response = {"is_success": True, "msg": ""}
    except Exception as e:
        response = {"is_success": False, "msg": f"An exception was raised: {e}"}
    return JsonResponse(response)


@logged_in_user
@require_POST
def assumption_delete(request, assumption_id):
    try:
        is_success = True
        msg = "Assumption deleted successfully."
        assumption = get_object_or_404(
            Assumption, pk=assumption_id, organization=request.user.organization
        )
        assumption.delete()
        # messages.success(request, "Assumption deleted successfully.")
    except Exception as e:
        is_success = False
        msg = "There was an issue deleting that assumption."
        # messages.error(request, "There was an issue deleting that assumption.")
        # TODO: proper logging
        print(
            f"assumption_delete Exception. user: {request.user}, assumption: {assumption_id}.",
            e,
        )
    return JsonResponse({"is_success": is_success, "msg": msg})
