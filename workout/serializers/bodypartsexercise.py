from rest_framework import serializers
from workout.models import BodyPartExercise


class BodyPartsExerciseSerializer(serializers.ModelSerializer):
    # read only nested serializers - will cause an N + 1 query problem
    # so instead using a PrimaryKeyRelatedField that will return only the IDs
    body_part = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    exercise = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = BodyPartExercise
        fields = ["body_part", "exercise"]
