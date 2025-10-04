from pydantic import BaseModel, ConfigDict
from workout.models import Exercise
from django.shortcuts import get_object_or_404


class ExerciseModel(BaseModel):
    name: str
    description: str
    sets: int
    reps: int
    weight: float

    model_config = ConfigDict(from_attributes=True)



