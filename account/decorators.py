# Django
from django.shortcuts import redirect
from django.urls import resolve, reverse
from urllib.parse import urlencode


def authenticated_user(view_func):
    """A decorator that checks if the user is already authenticated.

    Parameters
    ----------
    view_func
        This decorator passes in the view function.

    Logic
    -----
    - If the user is authenticated, go to strategy:business_problem_all, else return the view.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("strategy:business_problem_all")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def logged_in_user(view_func):
    """A decorator that checks if the user is logged in and properly configured.

    Parameters
    ----------
    view_func
        This decorator passes in the view function.

    Logic
    -----
    - If the user is authenticated and has an organization (and isn't in the
        process of signing up), return the view.
    - If the user is authenticated and does not have an organization, redirect
        them to account:organization_signup.
    - Else, return them to login.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if (
                not request.user.organization
                and resolve(request.path_info).url_name != "organization_create"
            ):
                return redirect("account:organization_create")
            else:
                return view_func(request, *args, **kwargs)
        else:
            base_url = reverse("account:login")
            querystring = urlencode({"next": request.path})
            url = f"{base_url}?{querystring}"
            return redirect(url)

    return wrapper_func
