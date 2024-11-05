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
from project.models import Project
from strategy.forms import (
    PlanningEventCreateForm,
    PlanningEventEditForm,
    CriterionWeightCreateForm,
    BusinessProblemScoreForm,
    CriterionWeightEditForm,
    PlanningEventBusinessProblemAssociateForm,
)
from strategy.models import (
    PlanningEvent,
    Strategy,
    CriterionWeight,
    PlanningEventBusinessProblem,
    BusinessProblemScore,
    PlanningEventStrategy,
    StrategyScore,
    PlanningEventProject,
    ProjectScore
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
    ).order_by("-is_chosen", "rank", "-final_score")
    strategies = PlanningEventStrategy.objects.filter(
        planning_event=planning_event
    ).order_by("-is_chosen", "rank", "-final_score")
    projects = PlanningEventProject.objects.filter(
        planning_event=planning_event
    ).order_by("-is_chosen", "rank", "-final_score")
    context = {
        "event": planning_event,
        "criteria": criteria,
        "business_problems": business_problems,
        "strategies": strategies,
        "projects": projects
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
            planning_event_id=planning_event.pk,
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
        criterion_type = None
        try:
            form = CriterionWeightCreateForm(request.POST)
            if form.is_valid():
                criterion_weight = form.save()
                is_success = True
                pk = criterion_weight.pk
                criterion_type = criterion_weight.criterion.get_criterion_type_display()
                action = reverse(
                    "strategy:criterion_weight_delete",
                    kwargs={
                        "planning_event_id": planning_event.pk,
                        "criterion_weight_id": pk,
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
                f"criterion_weight_create Exception. user: {request.user}, "
                f"planning_event_id: {planning_event_id}.",
                e,
            )
        json_response = {
            "is_success": is_success,
            "msg": msg,
            "pk": pk,
            "action": action,
            "criterion_type": criterion_type,
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
@require_http_methods(["GET", "POST"])
def criterion_weight_edit(request, planning_event_id, criterion_weight_id):
    planning_event = get_object_or_404(
        PlanningEvent, pk=planning_event_id, organization=request.user.organization
    )
    criterion_weight = get_object_or_404(
        CriterionWeight, pk=criterion_weight_id, planning_event=planning_event
    )
    if request.method == "POST":
        form = CriterionWeightEditForm(request.POST, instance=criterion_weight)
        if form.is_valid():
            criterion_weight = form.save()
            is_success = True
            msg = "Update successful!"
            weight = criterion_weight.weight
            pk = criterion_weight.pk
        else:
            is_success = False
            msg = "There was an issue deleting that criterion."
            weight = None
            pk = None

        return JsonResponse(
            {"is_success": is_success, "msg": msg, "weight": weight, "pk": pk}
        )
    else:
        initial = {"modified_by": request.user}
        form = CriterionWeightEditForm(instance=criterion_weight, initial=initial)
        context = {
            "body": render_to_string(
                "base_form.html",
                {
                    "form": form,
                    "url": reverse(
                        "strategy:criterion_weight_edit",
                        kwargs={
                            "planning_event_id": planning_event_id,
                            "criterion_weight_id": criterion_weight_id,
                        },
                    ),
                    "form_id": "criterion-weight-edit-form",
                    "button": "Update",
                },
                request=request,
            ),
            "title": "Update criterion weight",
        }
        return JsonResponse(context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def criterion_weight_delete(request, planning_event_id, criterion_weight_id):
    try:
        is_success = True
        msg = "Criterion deleted successfully."
        planning_event = get_object_or_404(
            PlanningEvent, pk=planning_event_id, organization=request.user.organization
        )
        criterion_weight = get_object_or_404(
            CriterionWeight, pk=criterion_weight_id, planning_event=planning_event
        )
        criterion_weight.delete()
    except Exception as e:
        is_success = False
        msg = "There was an issue deleting that criterion."
        # messages.error(request, "There was an issue deleting that assumption.")
        # TODO: proper logging
        print(
            f"criterion_weight_delete Exception. user: {request.user}, criterion_weight_id: {criterion_weight_id}.",
            e,
        )
    return JsonResponse({"is_success": is_success, "msg": msg})


@logged_in_user
@require_http_methods(["GET", "POST"])
def planning_event_business_problem_associate(request, planning_event_id):
    planning_event = get_object_or_404(
        PlanningEvent, id=planning_event_id, organization=request.user.organization
    )
    business_problem_ids = PlanningEventBusinessProblem.objects.filter(
        planning_event=planning_event
    ).values_list("business_problem_id", flat=True)
    if request.method == "POST":
        form = PlanningEventBusinessProblemAssociateForm(
            request.POST, request=request, business_problem_ids=business_problem_ids
        )
        if form.is_valid():
            peba = form.save()
            is_success = True
            msg = "Update successful!"
            summary = peba.business_problem.summary
            business_problem_id = peba.business_problem.id
            action = reverse(
                "strategy:planning_event_business_problem_delete",
                kwargs={
                    "planning_event_id": planning_event.pk,
                    "business_problem_id": business_problem_id,
                },
            )
        else:
            # TODO: Error logging
            is_success = False
            msg = "There was an issue adding that business problem."
            summary = None
            business_problem_id = None
            action = None

        return JsonResponse(
            {
                "is_success": is_success,
                "msg": msg,
                "summary": summary,
                "business_problem_id": business_problem_id,
                "action": action,
            }
        )
    else:
        initial = {"planning_event": planning_event}
        form = PlanningEventBusinessProblemAssociateForm(
            initial=initial, request=request, business_problem_ids=business_problem_ids
        )
        context = {
            "body": render_to_string(
                "base_form.html",
                {
                    "form": form,
                    "url": reverse(
                        "strategy:planning_event_business_problem_associate",
                        kwargs={
                            "planning_event_id": planning_event_id,
                        },
                    ),
                    "form_id": "business-problem-associate-form",
                    "button": "Add",
                },
                request=request,
            ),
            "title": "Add business problem",
        }
        return JsonResponse(context)


@logged_in_user
@require_POST
def planning_event_business_problem_delete(
    request, planning_event_id, business_problem_id
):
    try:
        is_success = True
        msg = "Business problem removed successfully."
        planning_event_business_problem = get_object_or_404(
            PlanningEventBusinessProblem,
            planning_event_id=planning_event_id,
            business_problem_id=business_problem_id,
            planning_event__organization=request.user.organization,
            business_problem__organization=request.user.organization,
        )
        planning_event_business_problem.delete()
    except Exception as e:
        is_success = False
        msg = "There was an issue removing that business problem."
        # TODO: proper logging
        print(
            f"planning_event_business_problem_delete Exception. user: {request.user}, planning_event_id: {planning_event_id}. business_problem_id: {business_problem_id}.",
            e,
        )
    return JsonResponse({"is_success": is_success, "msg": msg})


@logged_in_user
@require_http_methods(["GET", "POST"])
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

                final_score_updates = []
                for pebp in planning_event_bps:
                    pebp.final_score = pebp.get_calculated_score()
                    final_score_updates.append(pebp)

                PlanningEventBusinessProblem.objects.bulk_update(
                    final_score_updates, ["final_score"]
                )

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


@logged_in_user
@require_POST
def planning_event_business_problem_set_rank(request, planning_event_id):
    is_success = True
    msg = ""
    order = {}
    try:
        planning_event_bps = PlanningEventBusinessProblem.objects.filter(
            planning_event_id=planning_event_id,
            planning_event__organization=request.user.organization,
        )
        order = {
            o: i for i, o in enumerate(request.POST.getlist("new_order[]", []), start=1)
        }
        updated_planning_events = []
        for pebps in planning_event_bps:
            if pebps.rank != order[str(pebps.pk)]:
                pebps.rank = order[str(pebps.pk)]
                updated_planning_events.append(pebps)
        PlanningEventBusinessProblem.objects.bulk_update(
            updated_planning_events, ["rank"]
        )
    except Exception as e:
        # TODO: Proper exception handling/logging
        is_success = False
        msg = f"Error updating rank. {e}"
    result = {"is_success": is_success, "msg": msg, "order": order}
    return JsonResponse(result)


@logged_in_user
@require_POST
def planning_event_business_problem_choose(request, planning_event_id):
    selected_ids = request.POST.getlist("selected_ids[]")
    updates = []
    try:
        # Update PlanningEventBusinessProblems
        planning_event = PlanningEvent.objects.get(
            pk=planning_event_id, organization=request.user.organization
        )
        selected_pebps = PlanningEventBusinessProblem.objects.filter(
            id__in=selected_ids, planning_event=planning_event
        ).order_by("-final_score")
        for i, pebp in enumerate(selected_pebps, start=1):
            pebp.rank = i
            pebp.is_chosen = True
            updates.append(pebp)

        unselected_pebps = (
            PlanningEventBusinessProblem.objects.filter(planning_event=planning_event)
            .exclude(id__in=selected_ids)
            .order_by("-final_score")
        )
        for i, pebp in enumerate(unselected_pebps, start=len(selected_pebps) + 1):
            pebp.rank = i
            pebp.is_chosen = False
            updates.append(pebp)

        PlanningEventBusinessProblem.objects.bulk_update(updates, ["rank", "is_chosen"])

        # Create or update PlanningEventStrategy
        create_strategies = Strategy.objects.filter(
            business_problems__in=[x.business_problem for x in selected_pebps]
        )
        delete_strategies = PlanningEventStrategy.objects.filter(planning_event=planning_event).exclude(strategy__in=create_strategies)
        for strategy in create_strategies:
            try:
                obj = PlanningEventStrategy.objects.get(planning_event=planning_event, strategy=strategy)
            except PlanningEventStrategy.DoesNotExist:
                obj = PlanningEventStrategy.objects.create(planning_event=planning_event, strategy=strategy)

        delete_strategies.delete()

        ret = {"is_success": True, "msg": ""}

    except Exception as e:
        ret = {
            "is_success": False,
            "msg": f"Something went wrong choosing those business problems. {e}",
        }

    return JsonResponse(ret)


@logged_in_user
@require_http_methods(["GET", "POST"])
def planning_event_strategy_score(request, planning_event_id):
    # Fetch the relevant Planning Event
    planning_event = get_object_or_404(
        PlanningEvent, id=planning_event_id, organization=request.user.organization
    )

    # Fetch all CriterionWeights and PlanningEventStrategies related to the event
    criterion_weights = CriterionWeight.objects.filter(planning_event=planning_event)
    planning_event_strategy = PlanningEventStrategy.objects.filter(
        planning_event=planning_event
    )

    # Prepare a dictionary of existing scores for easier lookup
    existing_scores = StrategyScore.objects.filter(
        planning_event_strategy__in=planning_event_strategy,
        scoring_user=request.user,
    )

    # Create a dictionary to easily retrieve existing scores by (PES ID, CriterionWeight ID)
    existing_scores_dict = {
        (score.planning_event_strategy_id, score.criterion_weight_id): score
        for score in existing_scores
    }

    if request.method == "POST":
        new_scores = []
        updated_scores = []

        # Start atomic transaction for saving
        try:
            with transaction.atomic():
                # Loop through all Business Problems and Criterion Weights
                for pes in planning_event_strategy:
                    for criterion_weight in criterion_weights:
                        # Construct the input name for the corresponding score
                        input_name = f"score_{pes.id}_{criterion_weight.id}"
                        score_value = request.POST.get(input_name)

                        if score_value:
                            score_value = int(score_value)
                            if 1 <= score_value <= 10:
                                # Check if the score already exists
                                existing_score = existing_scores_dict.get(
                                    (pes.id, criterion_weight.id)
                                )

                                if existing_score:
                                    # If the score exists, check if it needs updating
                                    if existing_score.score != score_value:
                                        existing_score.score = score_value
                                        updated_scores.append(existing_score)
                                else:
                                    # If the score does not exist, create a new one
                                    new_scores.append(
                                        StrategyScore(
                                            planning_event_strategy=pes,
                                            criterion_weight=criterion_weight,
                                            scoring_user=request.user,
                                            score=score_value,
                                        )
                                    )

                # Bulk create new scores
                if new_scores:
                    StrategyScore.objects.bulk_create(new_scores)

                # Bulk update existing scores
                if updated_scores:
                    StrategyScore.objects.bulk_update(updated_scores, ["score"])

                final_score_updates = []
                for pes in planning_event_strategy:
                    pes.final_score = pes.get_calculated_score()
                    final_score_updates.append(pes)

                PlanningEventStrategy.objects.bulk_update(
                    final_score_updates, ["final_score"]
                )

        except Exception as e:
            print(f"Error saving scores: {e}")

        return redirect(
            "strategy:planning_event_strategy_score",
            planning_event_id=planning_event_id,
        )

    # Pass data to template
    context = {
        "planning_event": planning_event,
        "criterion_weights": criterion_weights,
        "planning_event_strategy": planning_event_strategy,
        "scores_dict": existing_scores_dict,  # For displaying scores
    }

    return render(request, "strategy/planning_event_strategy.html", context)


@logged_in_user
@require_POST
def planning_event_strategy_choose(request, planning_event_id):
    selected_ids = request.POST.getlist("selected_ids[]")
    updates = []
    try:
        # Update PlanningEventStrategies
        planning_event = PlanningEvent.objects.get(
            pk=planning_event_id, organization=request.user.organization
        )
        selected_strategies = PlanningEventStrategy.objects.filter(
            id__in=selected_ids, planning_event=planning_event
        ).order_by("-final_score")
        for i, pes in enumerate(selected_strategies, start=1):
            pes.rank = i
            pes.is_chosen = True
            updates.append(pes)

        unselected_strategies = (
            PlanningEventStrategy.objects.filter(planning_event=planning_event)
            .exclude(id__in=selected_ids)
            .order_by("-final_score")
        )
        for i, pes in enumerate(unselected_strategies, start=len(selected_strategies) + 1):
            pes.rank = i
            pes.is_chosen = False
            updates.append(pes)

        PlanningEventStrategy.objects.bulk_update(updates, ["rank", "is_chosen"])

        # Create or update PlanningEventProject
        create_project = Project.objects.filter(
            strategy__in=[x.strategy for x in selected_strategies]
        )
        delete_project = PlanningEventProject.objects.filter(planning_event=planning_event).exclude(project__in=create_project)
        for project in create_project:
            try:
                obj = PlanningEventProject.objects.get(planning_event=planning_event, project=project)
            except PlanningEventProject.DoesNotExist:
                obj = PlanningEventProject.objects.create(planning_event=planning_event, project=project)

        delete_project.delete()

        ret = {"is_success": True, "msg": ""}

    except Exception as e:
        ret = {
            "is_success": False,
            "msg": f"Something went wrong choosing those strategies. {e}",
        }

    return JsonResponse(ret)


@logged_in_user
@require_http_methods(["GET", "POST"])
def planning_event_project_score(request, planning_event_id):
    # Fetch the relevant Planning Event
    planning_event = get_object_or_404(
        PlanningEvent, id=planning_event_id, organization=request.user.organization
    )

    # Fetch all CriterionWeights and PlanningEventProjects related to the event
    criterion_weights = CriterionWeight.objects.filter(planning_event=planning_event)
    planning_event_project = PlanningEventProject.objects.filter(
        planning_event=planning_event
    )

    # Prepare a dictionary of existing scores for easier lookup
    existing_scores = ProjectScore.objects.filter(
        planning_event_project__in=planning_event_project,
        scoring_user=request.user,
    )

    # Create a dictionary to easily retrieve existing scores by (PES ID, CriterionWeight ID)
    existing_scores_dict = {
        (score.planning_event_project_id, score.criterion_weight_id): score
        for score in existing_scores
    }

    if request.method == "POST":
        new_scores = []
        updated_scores = []

        # Start atomic transaction for saving
        try:
            with transaction.atomic():
                # Loop through all Business Problems and Criterion Weights
                for pep in planning_event_project:
                    for criterion_weight in criterion_weights:
                        # Construct the input name for the corresponding score
                        input_name = f"score_{pep.id}_{criterion_weight.id}"
                        score_value = request.POST.get(input_name)

                        if score_value:
                            score_value = int(score_value)
                            if 1 <= score_value <= 10:
                                # Check if the score already exists
                                existing_score = existing_scores_dict.get(
                                    (pep.id, criterion_weight.id)
                                )

                                if existing_score:
                                    # If the score exists, check if it needs updating
                                    if existing_score.score != score_value:
                                        existing_score.score = score_value
                                        updated_scores.append(existing_score)
                                else:
                                    # If the score does not exist, create a new one
                                    new_scores.append(
                                        ProjectScore(
                                            planning_event_project=pep,
                                            criterion_weight=criterion_weight,
                                            scoring_user=request.user,
                                            score=score_value,
                                        )
                                    )

                # Bulk create new scores
                if new_scores:
                    ProjectScore.objects.bulk_create(new_scores)

                # Bulk update existing scores
                if updated_scores:
                    ProjectScore.objects.bulk_update(updated_scores, ["score"])

                final_score_updates = []
                for pep in planning_event_project:
                    pep.final_score = pep.get_calculated_score()
                    final_score_updates.append(pep)

                PlanningEventProject.objects.bulk_update(
                    final_score_updates, ["final_score"]
                )

        except Exception as e:
            print(f"Error saving scores: {e}")

        return redirect(
            "strategy:planning_event_project_score",
            planning_event_id=planning_event_id,
        )

    # Pass data to template
    context = {
        "planning_event": planning_event,
        "criterion_weights": criterion_weights,
        "planning_event_project": planning_event_project,
        "scores_dict": existing_scores_dict,  # For displaying scores
    }

    return render(request, "strategy/planning_event_project.html", context)


@logged_in_user
@require_POST
def planning_event_project_choose(request, planning_event_id):
    selected_ids = request.POST.getlist("selected_ids[]")
    updates = []
    try:
        # Update PlanningEventProjects
        planning_event = PlanningEvent.objects.get(
            pk=planning_event_id, organization=request.user.organization
        )
        selected_projects = PlanningEventProject.objects.filter(
            id__in=selected_ids, planning_event=planning_event
        ).order_by("-final_score")
        for i, pebp in enumerate(selected_projects, start=1):
            pebp.rank = i
            pebp.is_chosen = True
            updates.append(pebp)

        unselected_projects = (
            PlanningEventProject.objects.filter(planning_event=planning_event)
            .exclude(id__in=selected_ids)
            .order_by("-final_score")
        )
        for i, pebp in enumerate(unselected_projects, start=len(selected_projects) + 1):
            pebp.rank = i
            pebp.is_chosen = False
            updates.append(pebp)

        PlanningEventProject.objects.bulk_update(updates, ["rank", "is_chosen"])

        ret = {"is_success": True, "msg": ""}

    except Exception as e:
        ret = {
            "is_success": False,
            "msg": f"Something went wrong choosing those strategies. {e}",
        }

    return JsonResponse(ret)