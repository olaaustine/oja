from rest_framework import serializers
from workout.models import BodyPart, Exercise
from typing import Optional
from workout.serializers.bodyparts import BodyPartSerializer
from workout.serializers.exercise import ExerciseSerializer
from workout.models import BodyPartExercise, BodyPart, Exercise


class BodyPartsExerciseSerializer(serializers.ModelSerializer):
    # read only nested serializers
    body_part = BodyPartSerializer(read_only=True)
    exercise = ExerciseSerializer(read_only=True)


    class Meta:
        model = BodyPartExercise
        fields = ['body_part', 'exercise']

