# Django
from django.db import models

# App
from strategyapp import settings
from account.models import Organization, Team, TimePeriod


class BusinessProblem(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
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
    is_public = models.BooleanField(default=True, verbose_name="public")
    category = models.CharField(
        max_length=20,
        choices=(("Problem", "Problem"), ("Opportunity", "Opportunity")),
        default="Problem",
    )
    time_period = models.ForeignKey(
        TimePeriod, on_delete=models.SET_NULL, null=True, blank=True
    )


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
    is_chosen = models.BooleanField(default=False)
    time_period = models.ForeignKey(
        TimePeriod, on_delete=models.SET_NULL, null=True, blank=True
    )
    # Voting mechanism


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
    business_problem = models.ForeignKey(BusinessProblem, on_delete=models.CASCADE)
    strategies = models.ManyToManyField(Strategy)
