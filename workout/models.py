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
        ordering = ['name']
        verbose_name = 'exercise'
        verbose_name_plural = 'exercises'

class BodyPart(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'body part'
        verbose_name_plural = 'body parts'

class BodyPartExercise(models.Model):
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.body_part.name} - {self.exercise.name}"

    class Meta:
        unique_together = ('body_part', 'exercise')
        verbose_name = 'body part exercise'
        verbose_name_plural = 'body part exercises'

class WorkoutSession(models.Model):
    date = models.DateField(auto_now_add=True)
    body_part_exercise = models.ForeignKey(BodyPartExercise, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Workout Session on {self.date}. You worked on {self.body_part.name} with {self.exercise.name}"

    class Meta:
        ordering = ['-date']
        unique_together = ('date', 'body_part_exercise')
        verbose_name = 'workout sessions'

class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

class UserWorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s session on {self.date}"

    class Meta:
        ordering = ['-date']
        db_table = 'user_workout_session'
        verbose_name = 'user workout session'
        verbose_name_plural = 'user workout sessions'