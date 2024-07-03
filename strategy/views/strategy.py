# Django
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

# App
from strategy.forms import StrategyCreateForm, StrategyEditForm
from strategy.models import BusinessProblem, Strategy, Assumption


def strategy_create(request):
    if request.method == "POST":
        form = StrategyCreateForm(request.POST)
        if form.is_valid():
            problem = get_object_or_404(
                BusinessProblem,
                pk=form.cleaned_data["problem"],
                organization=request.user.organization,
            )
            strategy = form.save()
            strategy.business_problems.add(problem)
            messages.success(request, "Strategy created successfully!")
            return redirect(
                "strategy:business_problem_detail", business_problem_id=problem.pk
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        business_problem_id = request.GET.get("business_problem_id")
        problem = get_object_or_404(
            BusinessProblem,
            pk=business_problem_id,
            organization=request.user.organization,
        )
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
            "problem": problem.pk,
        }
        form = StrategyCreateForm(initial=initial)
        context = {
            "form": form,
            "url": reverse("strategy:strategy_create"),
            "form_id": "strategy-create-form",
            "button": "Create",
        }
        return render(request, "strategy/strategy_create.html", context)


@require_GET
def strategy_detail(request, strategy_id):
    strategy = get_object_or_404(
        Strategy, pk=strategy_id, organization=request.user.organization
    )
    context = {"strategy": strategy}
    return render(request, "strategy/strategy_detail.html", context)


def strategy_edit(request, strategy_id):
    strategy = get_object_or_404(
        Strategy, pk=strategy_id, organization=request.user.organization
    )
    if request.method == "POST":
        form = StrategyEditForm(request.POST, instance=strategy)
        if form.is_valid():
            strategy = form.save()
            messages.success(request, "Update successful!")
            return redirect("strategy:strategy_detail", strategy_id=strategy.pk)
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {"modified_by": request.user}
        form = StrategyEditForm(instance=strategy, initial=initial)
        context = {
            "form": form,
            "form_id": "strategy-edit-form",
            "url": reverse(
                "strategy:strategy_edit", kwargs={"strategy_id": strategy.pk}
            ),
            "button": "Update",
            "back_link": request.META.get(
                "HTTP_REFERER",
                reverse(
                    "strategy:strategy_detail", kwargs={"strategy_id": strategy.pk}
                ),
            ),
        }
        return render(request, "strategy/strategy_edit.html", context)


def strategy_delete(request, strategy_id):
    try:
        strategy = get_object_or_404(
            Strategy, pk=strategy_id, organization=request.user.organization
        )
        strategy.delete()
        messages.success(request, "Strategy deleted successfully.")
    except Exception as e:
        messages.error(request, "There was an issue deleting that strategy.")
        # TODO: proper logging
        print(
            f"strategy_delete Exception. user: {request.user}, strategy: {strategy_id}.",
            e,
        )
    return redirect("strategy:business_problem_all")