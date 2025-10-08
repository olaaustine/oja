import pytest
from django.urls import reverse
from workout.models import BodyPart, Exercise, BodyPartExercise, WorkoutSession, User


@pytest.mark.django_db
def test_add_body_part(client):
    url = reverse("create_body_part")
    response = client.get(url)
    assert response.status_code == 200
    assert b"<form" in response.content


@pytest.mark.django_db
def test_add_body_part_post_valid(client):
    url = reverse("create_body_part")
    data = {"name": "Legs", "description": "Lower body"}
    response = client.post(url, data)
    assert response.status_code == 200
    assert BodyPart.objects.filter(name="Legs").exists()
    assert b"success" in response.content


@pytest.mark.django_db
def test_add_body_part_post_invalid(client):
    url = reverse("create_body_part")
    data = {"name": "", "description": ""}
    response = client.post(url, data)
    assert response.status_code == 200
    assert not BodyPart.objects.filter(name="").exists()


@pytest.mark.django_db
def test_add_body_part_exercise(client, db):
    url = reverse("create_body_part_exercise")
    body_part = BodyPart.objects.create(name="Arms", description="Upper body")
    data = {
        "body_part": body_part.id,
        "exercise_name": "Arm exercise",
        "exercise_description": "",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert BodyPartExercise.objects.filter(body_part=body_part).exists()


@pytest.mark.django_db
def test_add_body_part_exercise_post_invalid(client):
    url = reverse("create_body_part_exercise")
    data = {"body_part": "", "exercise_name": "", "exercise_description": ""}
    response = client.post(url, data)
    assert response.status_code == 200
    assert not Exercise.objects.filter(name="").exists()


@pytest.mark.django_db
def test_add_workout_session(client):
    body_part = BodyPart.objects.create(name="Chest", description="Upper body")
    exercise = Exercise.objects.create(
        name="Bench Press", description="Chest exercise", weights=100, sets=3, reps=10
    )
    BodyPartExercise.objects.create(body_part=body_part, exercise=exercise)
    url = reverse("create_workout_session")
    response = client.get(url)
    assert response.status_code == 200
    assert b"<form" in response.content


@pytest.mark.django_db
def test_add_workout_session_post_valid(client):
    body_part = BodyPart.objects.create(name="Shoulders", description="Upper body")
    exercise = Exercise.objects.create(
        name="Shoulder Press",
        description="Shoulder exercise",
        weights=50,
        sets=4,
        reps=8,
    )
    bpe = BodyPartExercise.objects.create(body_part=body_part, exercise=exercise)
    user = User.objects.create(username="testuser")
    url = reverse("create_workout_session")
    data = {
        "body_part_exercise": bpe.id,
        "exercise_name": "Shoulder Press",
        "exercise_description": "Shoulder exercise",
        "exercise_weights": 50,
        "exercise_sets": 4,
        "exercise_reps": 8,
        "user": user.id,
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert WorkoutSession.objects.filter(body_part_exercise=bpe).exists()
    assert exercise.weights == 50
    assert exercise.sets == 4
    assert exercise.reps == 8
    assert b"success" in response.content


@pytest.mark.django_db
def test_add_workout_session_post_invalid(client):
    url = reverse("create_workout_session")
    data = {
        "user": "",
        "body_part_exercise": "",
        "exercise_name": "",
        "exercise_description": "",
        "exercise_weights": "",
        "exercise_sets": "",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert not WorkoutSession.objects.exists()


@pytest.mark.django_db
def test_edit_workout_session(client):
    workout_session = WorkoutSession.objects.create(
        body_part_exercise=BodyPartExercise.objects.create(
            body_part=BodyPart.objects.create(name="Test", description="Test desc"),
            exercise=Exercise.objects.create(
                name="Test Exercise",
                description="Test exercise desc",
                weights=20,
                sets=2,
                reps=15,
            ),
        ),
        user=User.objects.create(username="testuser"),
    )
    url = reverse("edit_workout_session", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["workout_session"] == workout_session


@pytest.mark.django_db
def test_get_exercise_details_api(client):
    body_part_exercise = BodyPartExercise.objects.create(
        body_part=BodyPart.objects.create(name="Test", description="Test desc"),
        exercise=Exercise.objects.create(
            name="Test Exercise",
            description="Test exercise desc",
            weights="20.00",
            sets=2,
            reps=15,
        ),
    )
    url = reverse("exercise_details", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == body_part_exercise.exercise.name
    assert data["description"] == body_part_exercise.exercise.description
    assert data["weights"] == body_part_exercise.exercise.weights
    assert data["sets"] == body_part_exercise.exercise.sets
    assert data["reps"] == body_part_exercise.exercise.reps
