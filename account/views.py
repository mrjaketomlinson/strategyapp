# Django
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
# App
from account.forms import UserCreationForm


def index(request):
    return render(request, "account/hi.html")


def signup(request):
    """View to sign up a new user."""

    context = {}
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("account:index")
        else:
            context["registration_form"] = form
    context["registration_form"] = UserCreationForm()
    return render(request, "account/signup.html", context)