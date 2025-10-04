from workout.models import WorkoutSession
from rest_framework import serializers
from workout.serializers.bodyparts import BodyPartSerializer
from workout.serializers.exercise import ExerciseSerializer

class WorkoutSessionSerializer(serializers.Serializer):
    date = serializers.DateField()
    body_parts = serializers.SerializerMethodField()
    exercises = serializers.SerializerMethodField()
    exercise_weights = serializers.SerializerMethodField()
    exercise_weights_increase_biweekly = serializers.SerializerMethodField()

    def get_body_parts(self, obj):
        return BodyPartSerializer(obj.body_part_exercise.body_part).data

    def get_exercises(self, obj):
        return ExerciseSerializer(obj.body_part_exercise.exercise).data

    def get_exercise_weights(self, obj):
        return obj.body_part_exercise.exercise.weights

    def get_exercise_weights_increase_biweekly(self, obj):
        sessions = WorkoutSession.objects.filter(
            body_part_exercise__exercise=obj.body_part_exercise.exercise
        ).order_by('-date')[:2]
        weights = [session.body_part_exercise.exercise.weights for session in sessions]
        return self.do_the_biweekly_calculation(weights)

    def do_the_biweekly_calculation(self, weights: list)-> float:
        if len(weights) >= 2:
            return weights[0] - weights[1]
        elif len(weights) == 1:
            return 0
        else:
            return 0

    def get_exercise_sets(self, obj):
        return obj.body_part_exercise.exercise.sets

    def get_exercise_reps(self, obj):
        return obj.body_part_exercise.exercise.reps


    class Meta:
        model = WorkoutSession
        fields = ['date', 'body_parts', 'exercises', 'exercise_weights', 'exercise_weights_biweekly']
