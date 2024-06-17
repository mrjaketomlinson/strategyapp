from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


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

    def __str__(self):
        return self.email
