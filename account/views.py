# Django
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import authenticated_user, logged_in_user
from account.forms import (
    UserCreationForm,
    UserLoginForm,
    OrganizationCreateForm,
    TeamCreateForm,
)
from account.models import Team


@authenticated_user
@require_GET
def index(request):
    return render(request, "account/hi.html")


@authenticated_user
@require_http_methods(["GET", "POST"])
def signup(request):
    """View to sign up a new user."""

    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.organization:
                return redirect("account:index")
            else:
                return redirect("account:organization_create")
        else:
            context["registration_form"] = form
    context["registration_form"] = UserCreationForm()
    return render(request, "account/signup.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def organization_create(request):
    if request.method == "POST":
        form = OrganizationCreateForm(request.POST)
        if form.is_valid():
            organization = form.save()
            user = request.user
            user.organization = organization
            user.save()
            return redirect("account:index")
    else:
        initial = {
            "name": request.user.get_email_domain().split(".")[0].capitalize(),
            "domain": request.user.get_email_domain(),
        }
        form = OrganizationCreateForm(initial=initial)
    context = {
        "form": form,
        "url": reverse("account:organization_create"),
        "form_id": "organization-create-form",
        "button": "Create",
    }
    return render(request, "account/organization_create.html", context)


@method_decorator(authenticated_user, name="dispatch")
class UserLogin(LoginView):
    authentication_form = UserLoginForm
    # template_name = "registration"


@logged_in_user
@require_GET
def team_all(request):
    teams = Team.objects.filter(organization=request.user.organization)
    context = {"teams": teams}
    return render(request, "account/team_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def team_create(request):
    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect("account:team_detail", team_id=team.pk)
    else:
        initial = {"members": request.user, "organization": request.user.organization}
        form = TeamCreateForm(initial=initial)
    context = {
        "form": form,
        "form_id": "team-create-form",
        "url": reverse("account:team_create"),
        "button": "Create",
    }
    return render(request, "account/team_create.html", context)


@logged_in_user
@require_GET
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id, organization=request.user.organization)
    context = {"team": team}
    return render(request, "account/team_detail.html", context)
