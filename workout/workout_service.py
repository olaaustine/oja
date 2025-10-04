from django.conf import settings
from pydantic import BaseModel, ConfigDict
from django.shortcuts import get_object_or_404
from openai import OpenAI
from workout.models import Exercise, BodyPartExercise
from workout.serializers.workout_session import WorkoutSessionSerializer


class ExerciseModel(BaseModel):
    """ Pydantic model for Exercise"""
    name: str
    description: str
    sets: int
    reps: int
    weight: float

    model_config = ConfigDict(from_attributes=True)


def get_exercise_by_id(exercise_id: int) -> ExerciseModel | None:
    """ Get an exercise by its ID and return it as an ExerciseModel """
    try:
        exercise = get_object_or_404(Exercise, id=exercise_id)
        return ExerciseModel.model_validate(exercise)
    except Exercise.DoesNotExist:
        return None

def get_all_workout_sessions_by_id(exercise_id: int):
    """ Get all workout sessions for a given BodyPartExercise ID """
    try:
        bodypart_exercise = get_object_or_404(BodyPartExercise, id=exercise_id)
        workout_sessions = bodypart_exercise.workoutsession_set.all()
        return WorkoutSessionSerializer(workout_sessions, many=True).data
    except BodyPartExercise.DoesNotExist:
        return None


def get_suggestions_for_exercise(body_part: str):
    """Get exercise suggestions based on body part"""
    client = OpenAI(api_key=settings.WORKOUT_OPENAI)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a fitness expert. Provide exercise suggestions based on body parts."
            },
            {
                "role": "user",
                "content": f"Suggest 3 exercises for the {body_part}."
            }
        ],
        max_tokens=150,
        n=1,
    )

    # Extract the model output text
    return response.choices[0].message.content.strip()

