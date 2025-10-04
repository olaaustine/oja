import pytest
from workout.models import BodyPart, Exercise, BodyPartExercise
from workout.forms import BodyPartExerciseForm, WorkoutSessionForm

@pytest.mark.django_db
def test_body_part_exercise_form_creates_exercise():
    body_part = BodyPart.objects.create(name="Legs", description="Lower body")
    form_data = {
        'body_part': body_part.id,
        'exercise_name': 'Squat',
        'exercise_description': 'A leg exercise'
    }
    form = BodyPartExerciseForm(data=form_data)
    assert form.is_valid()
    bpe = form.save()
    assert bpe.exercise.name == 'Squat'
    assert bpe.exercise.description == 'A leg exercise'
    assert bpe.body_part == body_part

@pytest.mark.django_db
def test_workout_session_form_edits_exercise_fields():
    body_part = BodyPart.objects.create(name="Arms", description="Upper body")
    exercise = Exercise.objects.create(name="Curl", description="Bicep curl", weights=10, sets=3, reps=12)
    bpe = BodyPartExercise.objects.create(body_part=body_part, exercise=exercise)
    form_data = {
        'body_part_exercise': bpe.id,
        'exercise_name': exercise.name,
        'exercise_description': exercise.description,
        'exercise_weights': 15,
        'exercise_sets': 4,
        'exercise_reps': 10
    }
    form = WorkoutSessionForm(data=form_data)
    assert form.is_valid()
    session = form.save()
    exercise.refresh_from_db()
    assert exercise.weights == 15
    assert exercise.sets == 4
    assert exercise.reps == 10
    assert session.body_part_exercise == bpe

@pytest.mark.django_db
def test_body_part_exercise_form_invalid_data():
    form = BodyPartExerciseForm(data={})
    assert not form.is_valid()
    assert 'body_part' in form.errors
    assert 'exercise_name' in form.errors
    assert 'exercise_description' in form.errors
