from workout.models import Exercise
from rest_framework import serializers

class ExerciseSerializer(serializers.ModelSerializer):
    """ Serializer for Exercise model """
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    weights = serializers.FloatField()
    sets = serializers.IntegerField()
    reps = serializers.IntegerField()

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'weights', 'sets', 'reps']