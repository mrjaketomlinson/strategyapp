# Django
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# App
from strategyapp import settings
from account.models import Organization, Team, TimePeriod

# Python
import statistics


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


class PlanningEvent(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="planning_event_created_by",
    )
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="planning_event_modified_by",
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    time_period = models.ForeignKey(TimePeriod, on_delete=models.SET_NULL, null=True)
    score_type = models.CharField(
        max_length=50,
        choices=(
            ("individual", "Individual"),  # Only a single person can score
            ("team", "Team"),  # Multiple people can score
        ),
    )
    scoring_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    scoring_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    score_value_type = models.CharField(
        max_length=50,
        choices=(
            ("tshirt", "T-shirt"),  # 1, 5, 10
            ("fibonacci", "Fibonacci"),  # 1, 2, 3, 5, 8
            ("scale", "1-10 Scale"),  # 1-10
        ),
    )

    def __str__(self):
        return self.name


class Criterion(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="criterion_created_by",
    )
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="criterion_modified_by",
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    criterion_type = models.CharField(
        max_length=50,
        choices=(
            ("max", "Maximize"),  # Higher values are better
            ("min", "Minimize"),  # Lower values are better
        ),
    )

    def __str__(self):
        return self.name


class CriterionWeight(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="criterion_weight_created_by",
    )
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="criterion_weight_modified_by",
    )
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    planning_event = models.ForeignKey(PlanningEvent, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.criterion.name} - {self.planning_event}: {self.weight}"


class PlanningEventBusinessProblem(models.Model):
    planning_event = models.ForeignKey(PlanningEvent, on_delete=models.CASCADE)
    business_problem = models.ForeignKey(BusinessProblem, on_delete=models.CASCADE)
    is_chosen = models.BooleanField(default=False)
    override_score = models.PositiveIntegerField(null=True)
    final_score = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ["planning_event", "business_problem"]

    def get_calculated_score(self):
        calculated_score = None
        try:
            weighted_scores = [x.weighted_score() for x in self.scores.all()]
        except ValueError:
            weighted_scores = []
        if weighted_scores:
            calculated_score = statistics.fmean(weighted_scores)
        return calculated_score
    
    def save(self, *args, **kwargs):
        """
        Override save method to update final score whenever the object is saved.
        """
        if not self.override_score:
            self.final_score = self.get_calculated_score()
        else:
            self.final_score = self.override_score
        super().save(*args, **kwargs)


class PlanningEventStrategy(models.Model):
    planning_event = models.ForeignKey(PlanningEvent, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    is_chosen = models.BooleanField(default=False)
    override_score = models.PositiveIntegerField(null=True)
    final_score = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ["planning_event", "strategy"]

    def get_calculated_score(self):
        calculated_score = None
        try:
            weighted_scores = [x.weighted_score() for x in self.scores.all()]
        except ValueError:
            weighted_scores = []
        if weighted_scores:
            calculated_score = statistics.fmean(weighted_scores)
        return calculated_score

    def save(self, *args, **kwargs):
        """
        Override save method to update final score whenever the object is saved.
        """
        if not self.override_score:
            self.final_score = self.get_calculated_score()
        else:
            self.final_score = self.override_score
        super().save(*args, **kwargs)


class PlanningEventProject(models.Model):
    planning_event = models.ForeignKey(PlanningEvent, on_delete=models.CASCADE)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    is_chosen = models.BooleanField(default=False)
    override_score = models.PositiveIntegerField(null=True)
    final_score = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ["planning_event", "project"]

    def get_calculated_score(self):
        calculated_score = None
        try:
            weighted_scores = [x.weighted_score() for x in self.scores.all()]
        except ValueError:
            weighted_scores = []        
        if weighted_scores:
            calculated_score = statistics.fmean(weighted_scores)
        return calculated_score

    def save(self, *args, **kwargs):
        """
        Override save method to update final score whenever the object is saved.
        """
        if not self.override_score:
            self.final_score = self.get_calculated_score()
        else:
            self.final_score = self.override_score
        super().save(*args, **kwargs)


class BusinessProblemScore(models.Model):
    planning_event_business_problem = models.ForeignKey(PlanningEventBusinessProblem, on_delete=models.CASCADE, related_name='scores')
    criterion_weight = models.ForeignKey(CriterionWeight, on_delete=models.CASCADE)
    scoring_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def weighted_score(self):
        return self.score * self.criterion_weight.weight

    def __str__(self):
        return f"{self.planning_event_business_problem.pk} - {self.criterion_weight.criterion.name}: {self.score}"


class StrategyScore(models.Model):
    planning_event_strategy = models.ForeignKey(PlanningEventStrategy, on_delete=models.CASCADE, related_name='scores')
    criterion_weight = models.ForeignKey(CriterionWeight, on_delete=models.CASCADE)
    scoring_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def weighted_score(self):
        return self.score * self.criterion_weight.weight

    def __str__(self):
        return f"{self.planning_event_strategy.pk} - {self.criterion_weight.criterion.name}: {self.score}"
    

class ProjectScore(models.Model):
    planning_event_project = models.ForeignKey(PlanningEventProject, on_delete=models.CASCADE, related_name='scores')
    criterion_weight = models.ForeignKey(CriterionWeight, on_delete=models.CASCADE)
    scoring_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def weighted_score(self):
        return self.score * self.criterion_weight.weight

    def __str__(self):
        return f"{self.planning_event_project.pk} - {self.criterion_weight.criterion.name}: {self.score}"