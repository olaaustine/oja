from workout.models import BodyPart
from rest_framework import serializers

class BodyPartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)

    def get_body_parts(self, instance: BodyPart):
        try:
            return BodyPart.objects.all()
        except BodyPart.DoesNotExist:
            return None

    def get_body_part(self, pk: int):
        try:
            return BodyPart.objects.get(pk=pk)
        except BodyPart.DoesNotExist:
            return None

    def update(self, instance: BodyPart, validated_data: dict) -> BodyPart:
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    class Meta:
        model = BodyPart
        fields = ['name', 'description']