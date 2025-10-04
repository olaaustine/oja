from workout.models import Exercise
from rest_framework import serializers

class ExerciseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    weights = serializers.IntegerField()
    sets = serializers.IntegerField()
    reps = serializers.IntegerField()


    def create(self, validated_data: dict) -> Exercise:
        return Exercise.objects.create(**validated_data)

    def update(self, instance: Exercise, validated_data: dict) -> Exercise:

        instance.weights = validated_data.get('weights', instance.weights)
        instance.sets = validated_data.get('sets', instance.sets)
        instance.reps = validated_data.get('reps', instance.reps)
        instance.save()
        return instance


    class Meta:
        model = Exercise
        fields = ['name', 'description', 'weights', 'sets', 'reps']