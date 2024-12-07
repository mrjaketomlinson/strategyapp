# Django
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# App
from account.decorators import logged_in_user
from account.forms import TeamCreateForm, TeamEditForm, TeamMemberCreateForm
from account.models import Team, TeamMember


@logged_in_user
@require_GET
def team_all(request):
    teams = Team.objects.filter(organization=request.user.organization)
    context = {
        "teams": teams,
        "breadcrumbs": [
            {"title": "Admin", "url": reverse("account:admin")},
            {"title": "Teams", "url": reverse("account:team_all")},
        ],
    }
    return render(request, "account/team_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def team_create(request):
    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save()
            member = TeamMember.objects.create(
                team=team, user=request.user, role="Admin"
            )
            return redirect("account:team_detail", team_id=team.pk)
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
        }
        form = TeamCreateForm(initial=initial)
    context = {
        "form": form,
        "form_id": "team-create-form",
        "url": reverse("account:team_create"),
        "button": "Create",
    }
    return render(request, "account/team_create.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def team_edit(request, team_id):
    team = get_object_or_404(Team, pk=team_id, organization=request.user.organization)
    if request.method == "POST":
        form = TeamEditForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save()
            messages.success(request, "Update successful!")
            return redirect(
                "account:team_detail",
                team_id=team.pk,
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {"modified_by": request.user}
        form = TeamEditForm(instance=team, initial=initial)
        context = {
            "form": form,
            "form_id": "team_edit_form",
            "url": reverse(
                "account:team_edit",
                kwargs={"team_id": team.pk},
            ),
            "button": "Update",
        }
        return render(request, "account/team_edit.html", context)


@logged_in_user
@require_GET
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id, organization=request.user.organization)
    members = TeamMember.objects.filter(team=team)
    context = {
        "team": team,
        "members": members,
        "breadcrumbs": [
            {"title": "Admin", "url": reverse("account:admin")},
            {"title": "Teams", "url": reverse("account:team_all")},
            {
                "title": team.name,
                "url": reverse("account:team_detail", kwargs={"team_id": team_id}),
            },
        ],
    }
    return render(request, "account/team_detail.html", context)


@logged_in_user
@require_POST
def team_delete(request, team_id):
    try:
        team = get_object_or_404(
            Team,
            pk=team_id,
            organization=request.user.organization,
        )
        team.delete()
        messages.success(request, "Team deleted successfully.")
    except Exception as e:
        messages.error(request, "There was an issue deleting that team.")
        # TODO: proper logging
        print(
            f"team_delete Exception. user: {request.user}, team: {team_id}.",
            e,
        )
    return redirect("account:team_all")


@logged_in_user
@require_http_methods(["GET", "POST"])
def team_member_create(request, team_id):
    try:
        is_success = True
        msg = ""
        delete_action = ""
        edit_action = ""
        team = Team.objects.get(pk=team_id, organization=request.user.organization)
    except Team.DoesNotExist:
        msg = "Something went wrong trying to create that team member with this specific team."
        is_success = False
        # TODO: Proper error messaging
        print(
            f"team_member_create raised an exception. Team doesn't exist. User: {request.user.pk}. team_id: {team_id}."
        )
        json_response = {
            "is_success": is_success,
            "msg": msg,
            "delete_action": delete_action,
            "edit_action": edit_action,
        }
        return JsonResponse(json_response)
    if request.method == "POST":
        try:
            form = TeamMemberCreateForm(request.POST, request=request)
            if form.is_valid():
                team_member = form.save()
                delete_action = reverse(
                    "account:team_member_delete",
                    kwargs={"team_id": team.pk, "user_id": team_member.user.pk},
                )
                edit_action = reverse(
                    "account:team_member_edit",
                    kwargs={"team_id": team.pk, "user_id": team_member.user.pk},
                )
            else:
                is_success = False
                for err, message in form.errors.items():
                    msg += f'Field: {err}. Message: {"; ".join(m for m in message)}'
        except Exception as e:
            is_success = False
            msg = "There was an issue creating this team member."
            # TODO: proper logging
            print(
                f"team_member_create Exception. user: {request.user}, "
                f"team_id: {team_id}.",
                e,
            )
        json_response = {
            "is_success": is_success,
            "msg": msg,
            "delete_action": delete_action,
            "edit_action": edit_action,
        }
        return JsonResponse(json_response)
    else:
        initial = {
            "team": team,
        }
        form = TeamMemberCreateForm(initial=initial, request=request)
        url = reverse(
            "account:team_member_create",
            kwargs={"team_id": team_id},
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
def team_member_edit(request, team_id, user_id): ...


@logged_in_user
@require_POST
def team_member_delete(request, team_id, user_id):
    try:
        is_success = True
        msg = "Team member deleted successfully."
        team_member = TeamMember.objects.get(team__pk=team_id, user__pk=user_id)
        team_member.delete()
        # messages.success(request, "Assumption deleted successfully.")
    except Exception as e:
        is_success = False
        msg = "There was an issue removing that team member."
        # TODO: proper logging
        print(
            f"team_member_delete Exception. user: {request.user}, team_id: {team_id}, user_id: {user_id}.",
            e,
        )
    return JsonResponse({"is_success": is_success, "msg": msg})
