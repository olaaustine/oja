from django.conf import settings
from openai import OpenAI
from workout.models import Exercise, BodyPartExercise
from workout.serializers.workout_session import (
    WorkoutSessionSerializer,
    ExerciseSerializer,
)


def get_exercise_by_name_and_body_part(
    body: str, name: str
) -> ExerciseSerializer | None:
    """Get an exercise by its name and return it as an ExerciseModel."""
    exercise = BodyPartExercise.objects.filter(
        body_part__name=body, exercise__name=name
    ).first()
    return ExerciseSerializer(exercise).data if exercise else None


def get_exercise_by_id(exercise_id: int) -> ExerciseSerializer | None:
    """Get an exercise by its ID and return it as an ExerciseModel"""
    exercise = Exercise.objects.filter(id=exercise_id).first()
    return ExerciseSerializer(exercise).data if exercise else None


def get_all_workout_sessions_by_id(exercise_id: int):
    """Get all workout sessions for a given BodyPartExercise ID"""
    body_part = BodyPartExercise.objects.filter(id=exercise_id).first()
    workout_sessions = body_part.workoutsession_set.all() if body_part else []
    return (
        WorkoutSessionSerializer(workout_sessions, many=True).data
        if workout_sessions
        else None
    )


def get_suggestions_for_exercise(body_part: str):
    """Get exercise suggestions based on body part"""

    client = OpenAI(api_key=settings.WORKOUT_OPENAI)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a fitness expert. Provide exercise suggestions based on body parts.",
            },
            {"role": "user", "content": f"Suggest 5 exercises for the {body_part}."},
        ],
        max_tokens=150,
        n=1,
    )

    # Extract the model output text
    return response.choices[0].message.content.strip()
