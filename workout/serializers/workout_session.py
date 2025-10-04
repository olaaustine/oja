from workout.models import WorkoutSession
from rest_framework import serializers
from workout.serializers.bodyparts import BodyPartSerializer
from workout.serializers.exercise import ExerciseSerializer

class WorkoutSessionSerializer(serializers.Serializer):
    """ Serializer for WorkoutSession model """
    body_parts = serializers.SerializerMethodField()
    exercises = serializers.SerializerMethodField()
    exercise_weights = serializers.SerializerMethodField()
    exercise_weights_increase_biweekly = serializers.SerializerMethodField()

    def get_body_parts(self, obj: WorkoutSession):
        """ Return the body part associated with the workout session """
        return BodyPartSerializer(obj.body_part_exercise.body_part).data

    def get_exercises(self, obj: WorkoutSession):
        """ Return the exercise associated with the workout session """
        return ExerciseSerializer(obj.body_part_exercise.exercise).data

    def get_exercise_weights(self, obj: WorkoutSession):
        """ Return the weights associated with the exercise in the workout session """
        return obj.body_part_exercise.exercise.weights

    def get_exercise_weights_increase_biweekly(self, obj: WorkoutSession):
        """ Calculate the biweekly weight increase for the exercise in the workout session """
        sessions = WorkoutSession.objects.filter(
            body_part_exercise__exercise=obj.body_part_exercise.exercise
        ).order_by('-date')[:2]
        weights = [session.body_part_exercise.exercise.weights for session in sessions]
        return self.do_the_biweekly_calculation(weights)

    def do_the_biweekly_calculation(self, weights: list)-> float:
        """Helper function to calculate the biweekly weight increase"""
        if len(weights) >= 2:
            return weights[0] - weights[1]
        elif len(weights) == 1:
            return 0
        else:
            return 0

    def get_exercise_sets(self, obj: WorkoutSession):
        """ Return the sets associated with the exercise in the workout session """
        return obj.body_part_exercise.exercise.sets

    def get_exercise_reps(self, obj: WorkoutSession):
        """ Return the reps associated with the exercise in the workout session """
        return obj.body_part_exercise.exercise.reps


    class Meta:
        model = WorkoutSession
        fields = ['body_parts', 'exercises', 'exercise_weights', 'exercise_weights_biweekly']
