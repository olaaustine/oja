from workout.models import Exercise, BodyPart, WorkoutSession
from rest_framework import serializers
from workout.serializers.bodyparts import BodyPartSerializer
from workout.serializers.exercise import ExerciseSerializer

class WorkoutSessionSerializer(serializers.Serializer):
    date = serializers.DateField()
    body_parts = BodyPartSerializer(read_only=True)
    exercises = ExerciseSerializer(read_only=True)

    body_part_id = serializers.PrimaryKeyRelatedField(
        source="body_parts", queryset=BodyPart.objects.all(), write_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        source="exercises", queryset=Exercise.objects.all(), write_only=True)

    def create(self, validated_data: dict) -> WorkoutSession:
        return WorkoutSession.objects.create(**validated_data)

    class Meta:
        model = WorkoutSession
        fields = ['date', 'body_parts', 'exercises', 'body_part_id', 'exercise_id']


