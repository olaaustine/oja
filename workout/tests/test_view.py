import pytest
from django.urls import reverse
from workout.models import BodyPart, Exercise, BodyPartExercise, WorkoutSession

@pytest.mark.django_db
def test_add_body_part(client):
    url = reverse('create_body_part')
    response = client.get(url)
    assert response.status_code == 200
    assert b'<form' in response.content

@pytest.mark.django_db
def test_add_body_part_post_valid(client):
    url = reverse('create_body_part')
    data = {'name': 'Legs', 'description': 'Lower body'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert BodyPart.objects.filter(name='Legs').exists()
    assert b'success' in response.content

@pytest.mark.django_db
def test_add_body_part_post_invalid(client):
    url = reverse('create_body_part')
    data = {'name': '', 'description': ''}
    response = client.post(url, data)
    assert response.status_code == 200
    assert not BodyPart.objects.filter(name='').exists()

@pytest.mark.django_db
def test_add_body_part_exercise(client, db):
    body_part = BodyPart.objects.create(name='Arms', description='Upper body')
    url = reverse('create_body_part_exercise')
    response = client.get(url)
    assert response.status_code == 200
    assert b'<form' in response.content

@pytest.mark.django_db
def test_add_body_part_exercise_post_valid(client):
    body_part = BodyPart.objects.create(name='Back', description='Upper back')
    url = reverse('create_body_part_exercise')
    data = {
        'body_part': body_part.id,
        'exercise_name': 'Pull Up',
        'exercise_description': 'Back exercise'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert Exercise.objects.filter(name='Pull Up').exists()
    assert BodyPartExercise.objects.filter(body_part=body_part, exercise__name='Pull Up').exists()
    assert b'success' in response.content

@pytest.mark.django_db
def test_add_body_part_exercise_post_invalid(client):
    url = reverse('create_body_part_exercise')
    data = {'body_part': '', 'exercise_name': '', 'exercise_description': ''}
    response = client.post(url, data)
    assert response.status_code == 200
    assert not Exercise.objects.filter(name='').exists()

@pytest.mark.django_db
def test_add_workout_session(client):
    body_part = BodyPart.objects.create(name='Chest', description='Upper body')
    exercise = Exercise.objects.create(name='Bench Press', description='Chest exercise', weights=100, sets=3, reps=10)
    bpe = BodyPartExercise.objects.create(body_part=body_part, exercise=exercise)
    url = reverse('create_workout_session')
    response = client.get(url)
    assert response.status_code == 200
    assert b'<form' in response.content

@pytest.mark.django_db
def test_add_workout_session_post_valid(client):
    body_part = BodyPart.objects.create(name='Shoulders', description='Upper body')
    exercise = Exercise.objects.create(name='Shoulder Press', description='Shoulder exercise', weights=50, sets=4, reps=8)
    bpe = BodyPartExercise.objects.create(body_part=body_part, exercise=exercise)
    url = reverse('create_workout_session')
    data = {
        'body_part_exercise': bpe.id,
        'exercise_name': 'Shoulder Press',
        'exercise_description': 'Shoulder exercise',
        'exercise_weights': 60,
        'exercise_sets': 5,
        'exercise_reps': 12
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert WorkoutSession.objects.filter(body_part_exercise=bpe).exists()
    exercise.refresh_from_db()
    assert exercise.weights == 60
    assert exercise.sets == 5
    assert exercise.reps == 12
    assert b'success' in response.content

@pytest.mark.django_db
def test_add_workout_session_post_invalid(client):
    url = reverse('create_workout_session')
    data = {
        'body_part_exercise': '',
        'exercise_name': '',
        'exercise_description': '',
        'exercise_weights': '',
        'exercise_sets': '',
        'exercise_reps': ''
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert not WorkoutSession.objects.exists()
