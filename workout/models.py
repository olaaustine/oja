from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    weights = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "exercise"
        verbose_name_plural = "exercises"


class BodyPart(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "body part"
        verbose_name_plural = "body parts"


class BodyPartExercise(models.Model):
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.body_part.name} - {self.exercise.name}"

    class Meta:
        unique_together = ("body_part", "exercise")
        verbose_name = "body part exercise"
        verbose_name_plural = "body part exercises"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"


class WorkoutSession(models.Model):
    def get_user():
        return User.objects.first()

    def get_default_user():
        return User.objects.get()

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_user)
    date = models.DateField(auto_now_add=True)
    body_part_exercise = models.ForeignKey(
        BodyPartExercise, on_delete=models.CASCADE, default=1
    )

    def __str__(self):
        return f"Workout Session on {self.date}. You worked on {self.body_part.name} with {self.exercise.name}"

    class Meta:
        ordering = ["-date"]
        unique_together = ("date", "body_part_exercise", "user")
        verbose_name = "workout sessions"
