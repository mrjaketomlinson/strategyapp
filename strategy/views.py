# Django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# App
from strategy.forms import BusinessProblemCreateForm
from strategy.models import BusinessProblem, Strategy, Assumption



def business_problem_all(request):
    business_problems = BusinessProblem.objects.filter(organization=request.user.organization)
    context = {
        "business_problems": business_problems
    }
    return render(request, "strategy/business_problem_all.html", context)


def business_problem_create(request):
    if request.method == "POST":
        form = BusinessProblemCreateForm(request.POST)
        if form.is_valid():
            business_problem = form.save()
            return redirect("strategy:business_problem_detail", bp_id=business_problem.pk)
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user
        }
        form = BusinessProblemCreateForm(initial=initial)
        context = {
            "form": form,
            "form_id": "business_problem_create_form",
            "url": reverse("strategy:business_problem_create"),
            "button": "Create"
        }
        return render(request, "strategy/business_problem_create.html", context)


def business_problem_detail(request, bp_id):
    business_problem = get_object_or_404(BusinessProblem, pk=bp_id)
    context = {
        "problem": business_problem
    }
    return render(request, "strategy/business_problem_detail.html", context)


def strategy_detail(request):
    ...

