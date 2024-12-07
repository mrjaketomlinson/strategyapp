# Django
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods

# App
from account.decorators import authenticated_user, logged_in_user
from account.forms import (
    UserCreationForm,
    UserLoginForm,
    OrganizationCreateForm,
)
from account.models import User, Team


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
            return redirect("account:admin")
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
def admin(request):
    user_count = User.objects.filter(organization=request.user.organization).count()
    team_count = Team.objects.filter(organization=request.user.organization).count()
    context = {
        "user_count": user_count,
        "team_count": team_count
    }
    return render(request, "account/admin.html", context)


@logged_in_user
@require_GET
def user_all(request):
    users = User.objects.filter(organization=request.user.organization)
    context = {
        "users": users,
        "breadcrumbs": [
            {"title": "Admin", "url": reverse("account:admin")},
            {"title": "Users", "url": reverse("account:user_all")}
        ]
    }
    return render(request, "account/user_all.html", context)
