# Django
from django.db import models
# App
from strategyapp import settings
from account.models import Organization, Team



class BusinessProblem(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    team = models.ManyToManyField(Team)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    summary = models.CharField(max_length=255)
    description = models.TextField()


class Strategy(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    business_problem = models.ManyToManyField(BusinessProblem)


class Assumption(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    business_problem = models.ManyToManyField(BusinessProblem)
    strategy = models.ManyToManyField(Strategy)