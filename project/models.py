# Django
from django.db import models

# App
from account.models import Organization, Team, TimePeriod
from strategy.models import Strategy
from strategyapp import settings


class Project(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="project_created_by",
    )
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="project_modified_by",
    )
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    strategy = models.ForeignKey(
        Strategy,
        on_delete=models.SET_NULL,
        related_name="projects",
        related_query_name="project",
        null=True,
        blank=True
    )
    time_period = models.ForeignKey(
        TimePeriod, on_delete=models.SET_NULL, null=True, blank=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="project_owner",
    )
    working_group = models.ManyToManyField(settings.AUTH_USER_MODEL)


# class Kpi(models.Model):
#     summary = ...
#     description = ...
#     goal = ...
#     operator = ...


# class KpiUpdate(models.Model):
#     ...
