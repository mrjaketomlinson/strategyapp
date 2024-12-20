# Django
from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from strategy.forms import StrategyCreateForm, StrategyEditForm
from strategy.models import BusinessProblem, Strategy, Assumption


@logged_in_user
@require_GET
def strategy_all(request):
    strategies = Strategy.objects.filter(organization=request.user.organization)
    context = {
        "strategies": strategies,
    }
    return render(request, "strategy/strategy_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def strategy_create(request):
    if request.method == "POST":
        form = StrategyCreateForm(request.POST, request=request)
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
        form = StrategyCreateForm(initial=initial, request=request)
        context = {
            "form": form,
            "url": reverse("strategy:strategy_create"),
            "form_id": "strategy-create-form",
            "button": "Create",
        }
        return render(request, "strategy/strategy_create.html", context)


@logged_in_user
@require_GET
def strategy_detail(request, strategy_id):
    strategy = get_object_or_404(
        Strategy, pk=strategy_id, organization=request.user.organization
    )
    context = {"strategy": strategy}
    return render(request, "strategy/strategy_detail.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def strategy_edit(request, strategy_id):
    strategy = get_object_or_404(
        Strategy, pk=strategy_id, organization=request.user.organization
    )
    if request.method == "POST":
        form = StrategyEditForm(request.POST, instance=strategy, request=request)
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
        form = StrategyEditForm(instance=strategy, initial=initial, request=request)
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


@logged_in_user
@require_POST
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


@logged_in_user
@require_POST
def strategy_choose(request, strategy_id):
    is_success = True
    msg = ""
    strategy = None
    try:
        strategy = Strategy.objects.get(
            pk=strategy_id, organization=request.user.organization
        )
        is_chosen = False if strategy.is_chosen else True
        strategy.is_chosen = is_chosen
        strategy.save()
    except Strategy.DoesNotExist:
        is_success = False
        msg = "The strategy does not exist."
    except Exception as e:
        is_success = False
        msg = "There was an issue updating this strategy."
        # TODO: Proper logging
        print(
            f"strategy_choose Exception. user: {request.user}, strategy: {strategy_id}.",
            e,
        )
    return JsonResponse({"is_chosen": is_chosen, "is_success": is_success, "msg": msg})


@logged_in_user
@require_GET
def strategy_preview(request, strategy_id):
    is_success = True
    msg = ""
    title = ""
    body = ""
    footer = None
    try:
        strategy = Strategy.objects.get(
            pk=strategy_id, organization=request.user.organization
        )
        title = strategy.summary
        body = render_to_string(
            "strategy/strategy_preview.html", {"strategy": strategy}
        )
        footer = f'<a class="btn btn-primary" href="{reverse("strategy:strategy_detail", kwargs={"strategy_id": strategy.pk})}">View</a>'
    except Strategy.DoesNotExist:
        is_success = False
        msg = "The strategy does not exist."
    except Exception as e:
        is_success = False
        msg = "There was an issue getting this strategy."
        # TODO: Proper logging
        print(
            f"strategy_preview Exception. user: {request.user}, strategy: {strategy_id}.",
            e,
        )
    return JsonResponse(
        {
            "is_success": is_success,
            "msg": msg,
            "title": title,
            "body": body,
            "footer": footer,
        }
    )
