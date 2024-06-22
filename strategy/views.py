# Django
from django.shortcuts import render
# App
from strategy.models import BusinessProblem, Strategy, Assumption



def business_problem_all(request):
    business_problems = BusinessProblem.objects.filter(organization=request.user.organization)
    context = {
        "business_problems": business_problems
    }
    return render(request, "strategy/business_problem_all.html", context)


def business_problem_detail(request):
    ...


def strategy_detail(request):
    ...

