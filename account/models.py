# Django
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# Python
import re
from django.core.exceptions import ValidationError


def validate_domain(value):
    # Regular expression pattern to match a valid domain name
    pattern = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    if not re.match(pattern, value):
        raise ValidationError("Enter a valid domain name.")


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError("Users must have an email address.")
        if not first_name:
            raise ValueError("Users must have a first name.")
        if not last_name:
            raise ValueError("Users must have a last name.")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser (i.e., a user who can use the django admin)
        with the given email, name, and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """A user in the strategy application."""

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True
    )
    email = models.EmailField(
        verbose_name="email",
        max_length=60,
        unique=True,
    )
    date_joined = models.DateTimeField(
        verbose_name="date joined",
        auto_now_add=True,
    )
    last_login = models.DateTimeField(
        verbose_name="last login",
        auto_now=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    first_name = models.CharField(
        verbose_name="first name",
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=50,
    )
    timezone = models.CharField(
        max_length=100,
        verbose_name="time zone",
        default="US/Eastern",
        choices=(
            ("US/Alaska", "US/Alaska"),
            ("US/Aleutian", "US/Aleutian"),
            ("US/Arizona", "US/Arizona"),
            ("US/Central", "US/Central"),
            ("US/East-Indiana", "US/East-Indiana"),
            ("US/Eastern", "US/Eastern"),
            ("US/Hawaii", "US/Hawaii"),
            ("US/Indiana-Starke", "US/Indiana-Starke"),
            ("US/Michigan", "US/Michigan"),
            ("US/Mountain", "US/Mountain"),
            ("US/Pacific", "US/Pacific"),
            ("US/Samoa", "US/Samoa"),
        ),
    )

    # is_staff is for utilizing the Django admin
    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_email_domain(self):
        pattern = r"@([\w.-]+)$"
        match = re.search(pattern, self.email)
        if match:
            return match.group(1)
        else:
            return ""

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class Organization(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    domain = models.CharField(
        max_length=255,
        validators=[validate_domain],
        help_text="Enter a valid domain name (e.g., example.com).",
    )

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=(("Admin", "Admin"), ("Member", "Member"), ("Viewer", "Viewer")),
    )


class Team(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="team_created_by",
    )
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="team_modified_by",
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through=TeamMember)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TimePeriod(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="timeperiod_created_by",
    )
    modified_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="timeperiod_modified_by",
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

    def get_hierarchy(self):
        def build_tree(time_period):
            children = time_period.children.all().order_by(
                "start_date", "end_date", "name"
            )
            return {
                "name": time_period.name,
                "id": time_period.pk,
                "children": [build_tree(child) for child in children],
            }

        return build_tree(self)

    def get_ancestors(self):
        ancestors = []
        current = self.parent

        while current:
            ancestors.append(current)
            current = current.parent

        return ancestors

    def get_descendants(self):
        descendants = []

        def fetch_children(time_period):
            children = time_period.children.all().order_by(
                "start_date", "end_date", "name"
            )
            for child in children:
                descendants.append(child)
                fetch_children(child)

        fetch_children(self)
        return descendants
