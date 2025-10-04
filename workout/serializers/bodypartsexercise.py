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

    #write only primary key related fields
    body_part_id = serializers.PrimaryKeyRelatedField(
        source="body_part", queryset=BodyPart.objects.all(), write_only=True
    )
    exercise_id = serializers.PrimaryKeyRelatedField(
        source="exercise", queryset=Exercise.objects.all(), write_only=True
    )

    def create(self, validated_data: dict) -> BodyPartExercise:
        return BodyPartExercise.objects.create(**validated_data)

    class Meta:
        model = BodyPartExercise
        fields = ['body_part', 'exercise', 'body_part_id', 'exercise_id']

