from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from workout.models import User, Exercise, BodyPart, BodyPartExercise, WorkoutSession

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Exercise)
admin.site.register(BodyPart)
admin.site.register(BodyPartExercise)
admin.site.register(WorkoutSession)
# Register your models here.
