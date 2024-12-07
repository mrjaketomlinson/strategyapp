# Django
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from account.models import Team
from account.forms import *
from account.models import TimePeriod


@logged_in_user
@require_GET
def time_period_all(request):
    time_periods = TimePeriod.objects.filter(
        organization=request.user.organization
    ).order_by("start_date")
    context = {
        "time_periods": time_periods,
        "breadcrumbs": [
            {"title": "Admin", "url": reverse("account:admin")},
            {"title": "Time Periods", "url": reverse("account:time_period_all")},
        ],
    }
    return render(request, "account/time_period_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def time_period_create(request):
    if request.method == "POST":
        form = TimePeriodCreateForm(request.POST)
        if form.is_valid():
            time_period = form.save()
            messages.success(request, "Time period created successfully!")
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
        return redirect("account:time_period_all")
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
        }
        form = TimePeriodCreateForm(initial=initial, request=request)
        context = {
            "body": render_to_string(
                "base_form.html",
                {
                    "form": form,
                    "url": reverse("account:time_period_create"),
                    "form_id": "time-period-create-form",
                    "button": "Create",
                },
                request=request,
            ),
            "title": "Create new time period",
        }
        return JsonResponse(context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def time_period_edit(request, time_period_id):
    time_period = get_object_or_404(
        TimePeriod, pk=time_period_id, organization=request.user.organization
    )
    if request.method == "POST":
        form = TimePeriodEditForm(request.POST, instance=time_period)
        if form.is_valid():
            time_period = form.save()
            messages.success(request, "Update successful!")
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {"modified_by": request.user}
        form = TimePeriodEditForm(
            instance=time_period, initial=initial, request=request
        )
        context = {
            "body": render_to_string(
                "base_form.html",
                {
                    "form": form,
                    "url": reverse(
                        "account:time_period_edit",
                        kwargs={"time_period_id": time_period_id},
                    ),
                    "form_id": "time-period-edit-form",
                    "button": "Update",
                },
                request=request,
            ),
            "title": "Update time period",
        }
        return JsonResponse(context)


@logged_in_user
@require_GET
def time_period_detail(request, time_period_id):
    time_period = get_object_or_404(
        TimePeriod, pk=time_period_id, organization=request.user.organization
    )
    hierarchy = time_period.get_hierarchy()
    context = {
        "time_period": time_period,
        "hierarchy": hierarchy,
        "breadcrumbs": [
            {"title": "Admin", "url": reverse("account:admin")},
            {"title": "Time Periods", "url": reverse("account:time_period_all")},
            {
                "title": time_period.name,
                "url": reverse(
                    "account:time_period_detail",
                    kwargs={"time_period_id": time_period_id},
                ),
            },
        ],
    }
    return render(request, "account/time_period_detail.html", context)
