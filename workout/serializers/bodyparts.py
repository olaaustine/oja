from workout.models import BodyPart
from rest_framework import serializers

class BodyPartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)

    def get_body_parts(self, instance: BodyPart):
        """ Return all body parts """
        try:
            return BodyPart.objects.all()
        except BodyPart.DoesNotExist:
            return None

    def get_body_part(self, pk: int):
        """ Return a single body part by its ID """
        try:
            return BodyPart.objects.get(pk=pk)
        except BodyPart.DoesNotExist:
            return None

    class Meta:
        model = BodyPart
        fields = ['name', 'description']