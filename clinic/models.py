from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="RECEPTIONIST", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, role="ADMIN", **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        VET = "VET", "Vet"
        RECEPTIONIST = "RECEPTIONIST", "Receptionist"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RECEPTIONIST)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)


class Animal(models.Model):
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(default=0)
    owner_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class Vaccination(models.Model):
    animal = models.ForeignKey(Animal, related_name="vaccinations", on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=200)
    date_administered = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vaccine_name} for {self.animal.name} on {self.date_administered}"


class Reminder(models.Model):
    animal = models.ForeignKey(Animal, related_name="reminders", on_delete=models.CASCADE)
    vaccination = models.ForeignKey(Vaccination, related_name="reminders", on_delete=models.SET_NULL, null=True, blank=True)
    reminder_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.animal.name} on {self.reminder_date}"
