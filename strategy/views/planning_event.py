# Django
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from strategy.forms import (
    PlanningEventCreateForm,
    PlanningEventEditForm,
    CriterionWeightCreateForm,
    BusinessProblemScoreForm,
)
from strategy.models import (
    PlanningEvent,
    CriterionWeight,
    PlanningEventBusinessProblem,
    BusinessProblemScore,
)


@logged_in_user
@require_GET
def planning_event_all(request):
    planning_events = PlanningEvent.objects.filter(
        organization=request.user.organization
    ).order_by("name")
    context = {
        "planning_events": planning_events,
    }
    return render(request, "strategy/planning_event_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def planning_event_create(request):
    if request.method == "POST":
        form = PlanningEventCreateForm(request.POST)
        if form.is_valid():
            planning_event = form.save()
            messages.success(request, "Planning event created successfully!")
            return redirect(
                "strategy:planning_event_detail",
                kwargs={"planning_event_id": planning_event.pk},
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return redirect("strategy:planning_event_create")
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
        }
        form = PlanningEventCreateForm(initial=initial)
        context = {
            "form": form,
            "url": reverse("strategy:planning_event_create"),
            "form_id": "planning-event-create-form",
            "button": "Create",
        }
        return render(request, "strategy/planning_event_create.html", context)


@logged_in_user
@require_GET
def planning_event_detail(request, planning_event_id):
    planning_event = get_object_or_404(
        PlanningEvent, pk=planning_event_id, organization=request.user.organization
    )
    criteria = CriterionWeight.objects.filter(planning_event=planning_event)
    business_problems = PlanningEventBusinessProblem.objects.filter(
        planning_event=planning_event
    )
    context = {
        "event": planning_event,
        "criteria": criteria,
        "business_problems": business_problems,
    }
    return render(request, "strategy/planning_event_detail.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def planning_event_edit(request, planning_event_id):
    planning_event = get_object_or_404(
        PlanningEvent, pk=planning_event_id, organization=request.user.organization
    )
    if request.method == "POST":
        form = PlanningEventEditForm(request.POST, instance=planning_event)
        if form.is_valid():
            planning_event = form.save()
            messages.success(request, "Update successful!")
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
        return redirect(
            "strategy:planning_event_detail",
            kwargs={"planning_event_id": planning_event.pk},
        )
    else:
        initial = {"modified_by": request.user}
        form = PlanningEventEditForm(instance=planning_event, initial=initial)
        context = {
            "form": form,
            "url": reverse(
                "strategy:planning_event_edit",
                kwargs={"planning_event_id": planning_event_id},
            ),
            "form_id": "planning-event-edit-form",
            "button": "Update",
        }
        return render(request, "strategy/planning_event_edit.html", context)


@logged_in_user
@require_POST
def planning_event_delete(request, planning_event_id):
    try:
        planning_event = get_object_or_404(
            PlanningEvent,
            pk=planning_event_id,
            organization=request.user.organization,
        )
        planning_event.delete()
        messages.success(request, "Planning event deleted successfully.")
    except Exception as e:
        messages.error(request, "There was an issue deleting that planning event.")
        # TODO: proper logging
        print(
            f"planning_event_delete Exception. user: {request.user}, planning_event: {planning_event_id}.",
            e,
        )
    return redirect("strategy:planning_event_all")


@logged_in_user
@require_http_methods(["GET", "POST"])
def criterion_weight_create(request, planning_event_id):
    pk = None
    action = ""
    msg = ""
    is_success = False
    try:
        planning_event = PlanningEvent.objects.get(
            pk=planning_event_id, organization=request.user.organization
        )
    except PlanningEvent.DoesNotExist:
        msg = "Something went wrong trying to add a criteria with this specific planning event."
        # TODO: Proper error messaging
        print(
            f"criterion_weight_create raised an exception. PlanningEvent doesn't exist. User: {request.user.pk}. planning_event_id: {planning_event_id}."
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
            form = CriterionWeightCreateForm(request.POST)
            if form.is_valid():
                criterion_weight = form.save()
                is_success = True
                pk = criterion_weight.pk
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
                f"criterion_weight_create Exception. user: {request.user}, "
                f"planning_event_id: {planning_event_id}.",
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
            "created_by": request.user,
            "modified_by": request.user,
            "planning_event": planning_event,
        }
        form = CriterionWeightCreateForm(initial=initial)
        url = reverse(
            "strategy:criterion_weight_create",
            kwargs={"planning_event_id": planning_event_id},
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
def planning_event_business_problem_score(request, planning_event_id):
    # Fetch the relevant Planning Event
    planning_event = get_object_or_404(
        PlanningEvent, id=planning_event_id, organization=request.user.organization
    )

    # Fetch all CriterionWeights and PlanningEventBusinessProblems related to the event
    criterion_weights = CriterionWeight.objects.filter(planning_event=planning_event)
    planning_event_bps = PlanningEventBusinessProblem.objects.filter(
        planning_event=planning_event
    )

    # Prepare a dictionary of existing scores for easier lookup
    existing_scores = BusinessProblemScore.objects.filter(
        planning_event_business_problem__in=planning_event_bps,
        scoring_user=request.user,
    )

    # Create a dictionary to easily retrieve existing scores by (PEBP ID, CriterionWeight ID)
    existing_scores_dict = {
        (score.planning_event_business_problem_id, score.criterion_weight_id): score
        for score in existing_scores
    }

    if request.method == "POST":
        new_scores = []
        updated_scores = []

        # Start atomic transaction for saving
        try:
            with transaction.atomic():
                # Loop through all Business Problems and Criterion Weights
                for pebp in planning_event_bps:
                    for criterion_weight in criterion_weights:
                        # Construct the input name for the corresponding score
                        input_name = f"score_{pebp.id}_{criterion_weight.id}"
                        score_value = request.POST.get(input_name)

                        if score_value:
                            score_value = int(score_value)
                            if 1 <= score_value <= 10:
                                # Check if the score already exists
                                existing_score = existing_scores_dict.get(
                                    (pebp.id, criterion_weight.id)
                                )

                                if existing_score:
                                    # If the score exists, check if it needs updating
                                    if existing_score.score != score_value:
                                        existing_score.score = score_value
                                        updated_scores.append(existing_score)
                                else:
                                    # If the score does not exist, create a new one
                                    new_scores.append(
                                        BusinessProblemScore(
                                            planning_event_business_problem=pebp,
                                            criterion_weight=criterion_weight,
                                            scoring_user=request.user,
                                            score=score_value,
                                        )
                                    )

                # Bulk create new scores
                if new_scores:
                    BusinessProblemScore.objects.bulk_create(new_scores)

                # Bulk update existing scores
                if updated_scores:
                    BusinessProblemScore.objects.bulk_update(updated_scores, ["score"])

        except Exception as e:
            print(f"Error saving scores: {e}")

        return redirect(
            "strategy:planning_event_business_problem_score",
            planning_event_id=planning_event_id,
        )

    # Pass data to template
    context = {
        "planning_event": planning_event,
        "criterion_weights": criterion_weights,
        "planning_event_bps": planning_event_bps,
        "scores_dict": existing_scores_dict,  # For displaying scores
    }

    return render(request, "strategy/planning_event_business_problem.html", context)
