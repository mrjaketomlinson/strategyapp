# Django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from strategy.forms import BusinessProblemCreateForm, BusinessProblemEditForm
from strategy.models import BusinessProblem, Strategy, Assumption


@logged_in_user
@require_GET
def business_problem_all(request):
    business_problems = BusinessProblem.objects.filter(
        organization=request.user.organization
    )
    context = {"business_problems": business_problems}
    return render(request, "strategy/business_problem_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def business_problem_create(request):
    if request.method == "POST":
        form = BusinessProblemCreateForm(request.POST, request=request)
        if form.is_valid():
            business_problem = form.save()
            messages.success(request, "Business problem created successfully!")
            return redirect(
                "strategy:business_problem_detail",
                business_problem_id=business_problem.pk,
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
        }
        form = BusinessProblemCreateForm(initial=initial, request=request)
    context = {
        "form": form,
        "form_id": "business_problem_create_form",
        "url": reverse("strategy:business_problem_create"),
        "button": "Create",
    }
    return render(request, "strategy/business_problem_create.html", context)


@logged_in_user
@require_GET
def business_problem_detail(request, business_problem_id):
    business_problem = get_object_or_404(
        BusinessProblem, pk=business_problem_id, organization=request.user.organization
    )
    assumptions = business_problem.assumption_set.all()
    strategies = business_problem.strategy_set.all()
    context = {
        "problem": business_problem,
        "assumptions": assumptions,
        "strategies": strategies,
    }
    return render(request, "strategy/business_problem_detail.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def business_problem_edit(request, business_problem_id):
    business_problem = get_object_or_404(BusinessProblem, pk=business_problem_id)
    if request.method == "POST":
        form = BusinessProblemEditForm(request.POST, instance=business_problem, request=request)
        if form.is_valid():
            business_problem = form.save()
            messages.success(request, "Update successful!")
            return redirect(
                "strategy:business_problem_detail",
                business_problem_id=business_problem.pk,
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {"modified_by": request.user}
        form = BusinessProblemEditForm(instance=business_problem, initial=initial, request=request)
        context = {
            "form": form,
            "form_id": "business_problem_edit_form",
            "url": reverse(
                "strategy:business_problem_edit",
                kwargs={"business_problem_id": business_problem.pk},
            ),
            "button": "Update",
        }
        return render(request, "strategy/business_problem_edit.html", context)


@logged_in_user
@require_POST
def business_problem_delete(request, business_problem_id):
    try:
        business_problem = get_object_or_404(
            BusinessProblem,
            pk=business_problem_id,
            organization=request.user.organization,
        )
        business_problem.delete()
        messages.success(request, "Business problem deleted successfully.")
    except Exception as e:
        messages.error(request, "There was an issue deleting that business problem.")
        # TODO: proper logging
        print(
            f"business_problem_delete Exception. user: {request.user}, business_problem: {business_problem_id}.",
            e,
        )
    return redirect("strategy:business_problem_all")
