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
from project.forms import ProjectCreateForm, ProjectEditForm
from project.models import Project
from strategy.models import Strategy


@logged_in_user
@require_GET
def project_all(request):
    projects = Project.objects.filter(
        organization=request.user.organization
    )
    context = {"projects": projects}
    return render(request, "project/project_all.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def project_create(request, strategy_id):
    strategy = get_object_or_404(
        Strategy, pk=strategy_id, organization=request.user.organization
    )
    if request.method == "POST":
        form = ProjectCreateForm(request.POST, request=request)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project created successfully!")
            return redirect(
                "project:project_detail",
                project_id=project.pk,
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
    else:
        initial = {
            "organization": request.user.organization,
            "created_by": request.user,
            "modified_by": request.user,
            "strategy": strategy,
            "teams": Team.objects.filter(businessproblem__in=strategy.business_problems.all()).distinct()
        }
        form = ProjectCreateForm(initial=initial, request=request)
    context = {
        "form": form,
        "form_id": "project_create_form",
        "url": reverse("project:project_create", kwargs={"strategy_id": strategy_id}),
        "button": "Create",
    }
    return render(request, "project/project_create.html", context)


@logged_in_user
@require_GET
def project_detail(request, project_id):
    project = get_object_or_404(
        Project, pk=project_id, organization=request.user.organization
    )
    context = {"project": project}
    return render(request, "project/project_detail.html", context)


@logged_in_user
@require_http_methods(["GET", "POST"])
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id, organization=request.user.organization)
    if request.method == "POST":
        form = ProjectEditForm(request.POST, instance=project, request=request)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Update successful!")
            return redirect(
                "project:project_detail",
                project_id=project.pk,
            )
        else:
            for err, message in form.errors.items():
                messages.error(
                    request, f'Field: {err}. Message: {"; ".join(m for m in message)}'
                )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        initial = {"modified_by": request.user}
        form = ProjectEditForm(instance=project, initial=initial, request=request)
        context = {
            "form": form,
            "form_id": "project_edit_form",
            "url": reverse(
                "project:project_edit",
                kwargs={"project_id": project.pk},
            ),
            "button": "Update",
        }
        return render(request, "project/project_edit.html", context)
    

@logged_in_user
@require_POST
def project_delete(request, project_id):
    try:
        project = get_object_or_404(
            Project, pk=project_id, organization=request.user.organization
        )
        project.delete()
        messages.success(request, "Project deleted successfully.")
    except Exception as e:
        messages.error(request, "There was an issue deleting that project.")
        # TODO: proper logging
        print(
            f"project_delete Exception. user: {request.user}, project: {project_id}.",
            e,
        )
    return redirect("project:project_all")


@logged_in_user
@require_GET
def project_preview(request, project_id):
    is_success = True
    msg = ""
    title = ""
    body = ""
    footer = None
    try:
        project = Project.objects.get(
            pk=project_id, organization=request.user.organization
        )
        title = project.summary
        body = render_to_string("project/project_preview.html", {"project": project})
        footer = f'<a class="btn btn-primary" href="{reverse("project:project_detail", kwargs={"project_id": project.pk})}">View</a>'
    except Project.DoesNotExist:
        is_success = False
        msg = "The project does not exist."
    except Exception as e:
        is_success = False
        msg = "There was an issue getting this project."
        # TODO: Proper logging
        print(
            f"project_preview Exception. user: {request.user}, project: {project_id}.",
            e,
        )
    return JsonResponse({"is_success": is_success, "msg": msg, "title": title, "body": body, "footer": footer})