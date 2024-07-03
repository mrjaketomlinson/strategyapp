# Django
from django.db import models

# App
from strategyapp import settings
from account.models import Organization, Team


class BusinessProblem(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    team = models.ManyToManyField(Team)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="business_problem_created_by",
    )
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="business_problem_modified_by",
    )
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Strategy(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="strategy_created_by",
    )
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="strategy_modified_by",
    )
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    business_problems = models.ManyToManyField(BusinessProblem)


class Assumption(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="assumption_created_by",
    )
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="assumption_modified_by",
    )
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    business_problems = models.ManyToManyField(BusinessProblem)
    strategies = models.ManyToManyField(Strategy)
