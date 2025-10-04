from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from workout.models import Exercise, BodyPartExercise
from workout.forms import BodyPartForm, WorkoutSessionForm, BodyPartExerciseForm
from workout.workout_service import ExerciseModel
from workout.serializers.bodypartsexercise import BodyPartsExerciseSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class LandingPageView(TemplateView):
    template_name = "landing.html"

class BodyPartExerciseListTemplateView(ListView):
    model = BodyPartExercise
    template_name = "body_part_exercise_list.html"
    context_object_name = "object_list"



def get_exercise_details(request, id) -> Response:
    bodyparts_exercise = get_object_or_404(BodyPartExercise, id=id)
    exercise = get_object_or_404(Exercise, id=bodyparts_exercise.exercise.id)

    data = {
        "name": exercise.name,
        "description": exercise.description,
        "weights": exercise.weights,
        "sets": exercise.sets,
        "reps": exercise.reps,
    }
    return JsonResponse(data)


def add_body_part(request):
    if request.method == 'POST':
        form = BodyPartForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'create_body_part.html', {'form': form, 'success': True})
        else:
            return render(request, 'create_body_part.html', {'form': form, 'errors': form.errors})
    else:
        form = BodyPartForm()
    return render(request, 'create_body_part.html', {'form': form})


def add_body_part_exercise(request):
    if request.method == 'POST':
        form = BodyPartExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'create_body_part_exercise.html', {'form': form, 'success': True})
        else:
            return render(request, 'create_body_part_exercise.html', {'form': form, 'errors': form.errors})
    else:
        form = BodyPartExerciseForm()
    return render(request, 'create_body_part_exercise.html', {'form': form})


def add_workout_session(request):
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'create_session.html', {'form': form, 'success': True})
        else:
            return render(request, 'create_session.html', {'form': form, 'errors': form.errors})
    else:
        form = WorkoutSessionForm()
    return render(request, 'create_session.html', {'form': form})

def edit_workout_session(request, id):
    session = get_object_or_404(BodyPartExercise, id=id)
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return render(request, 'edit_session.html', {'form': form, 'success': True})
        else:
            return render(request, 'edit_session.html', {'form': form, 'errors': form.errors})
    else:
        form = WorkoutSessionForm(instance=session)
    return render(request, 'edit_session.html', {'form': form})
