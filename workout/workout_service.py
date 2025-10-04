from pydantic import BaseModel, ConfigDict
from workout.models import Exercise, BodyPartExercise
from django.shortcuts import get_object_or_404
from workout.serializers.workout_session import WorkoutSessionSerializer


class ExerciseModel(BaseModel):
    name: str
    description: str
    sets: int
    reps: int
    weight: float

    model_config = ConfigDict(from_attributes=True)


def get_exercise_by_id(exercise_id: int) -> ExerciseModel | None:
    try:
        exercise = get_object_or_404(Exercise, id=exercise_id)
        return ExerciseModel.model_validate(exercise)
    except Exercise.DoesNotExist:
        return None

def get_all_workout_sessions_by_id(exercise_id: int):
    try:
        bodypart_exercise = get_object_or_404(BodyPartExercise, id=exercise_id)
        workout_sessions = bodypart_exercise.workoutsession_set.all()
        return WorkoutSessionSerializer(workout_sessions, many=True).data
    except BodyPartExercise.DoesNotExist:
        return None



