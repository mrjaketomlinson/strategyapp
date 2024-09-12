# Django
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from strategy.forms import PlanningEventCreateForm, PlanningEventEditForm
from strategy.models import PlanningEvent


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
    context = {
        "event": planning_event
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
