from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from workout.models import Exercise, BodyPartExercise
from workout.forms import BodyPartForm, WorkoutSessionForm, BodyPartExerciseForm
from workout.workout_service import ExerciseModel, get_all_workout_sessions_by_id, get_suggestions_for_exercise
from workout.serializers.bodypartsexercise import BodyPartsExerciseSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse

class LandingPageView(TemplateView):
    """View for the landing page."""
    template_name = "landing.html"

class BodyPartExerciseListTemplateView(ListView):
    """View to list all BodyPartExercise entries."""
    model = BodyPartExercise
    template_name = "body_part_exercise_list.html"
    context_object_name = "object_list"

def get_exercise_details(request, id: int) -> JsonResponse:
    "Get exercise details by BodyPartExercise ID"
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

class WorkoutSessionsCalculations(APIView):
    """API view to get all workout sessions for a given exercise ID."""
    def get(self, request, exercise_id: int) -> Response:
        sessions = get_all_workout_sessions_by_id(exercise_id)
        if sessions is None:
            return Response({"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"sessions": sessions}, status=status.HTTP_200_OK)

def add_body_part(request) -> HttpResponse:
    """ View to add a new BodyPart """
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


def add_body_part_exercise(request) -> HttpResponse:
    suggestion = None
    if request.method == 'POST':
        form = BodyPartExerciseForm(request.POST)
        if form.is_valid():
            bodypart_exercise = form.save()
            # Get workout suggestion for the selected body part
            body_part_name = bodypart_exercise.body_part.name
            suggestion = get_suggestions_for_exercise(body_part_name)
            return render(request, 'create_body_part_exercise.html', {'form': form, 'success': True, 'suggestion': suggestion})
        else:
            return render(request, 'create_body_part_exercise.html', {'form': form, 'errors': form.errors})
    else:
        form = BodyPartExerciseForm()
    return render(request, 'create_body_part_exercise.html', {'form': form})


def add_workout_session(request) -> HttpResponse:
    """ View to add a new WorkoutSession along with editing related Exercise fields """
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            workout_session = form.save()
            return render(request, 'create_session.html', {'form': form, 'success': True, })
        else:
            return render(request, 'create_session.html', {'form': form, 'errors': form.errors})
    else:
        form = WorkoutSessionForm()
    return render(request, 'create_session.html', {'form': form})

def edit_workout_session(request, id) -> HttpResponse:
    """ View to edit an existing WorkoutSession along with related Exercise fields """
    summary_data = None
    try:
        bpe = BodyPartExercise.objects.get(id=id)
    except BodyPartExercise.DoesNotExist:
        return render(request, 'edit_session.html', {'form': None, 'errors': 'BodyPartExercise not found', 'summary_data': None})

    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            workout_session = form.save()
            summary_data = get_all_workout_sessions_by_id(bpe.exercise.id)
            return render(request, 'edit_session.html', {'form': form, 'success': True, 'summary_data': summary_data})
        else:
            if id:
                try:
                    bpe = BodyPartExercise.objects.get(id=body_part_exercise_id)
                    summary_data = get_all_workout_sessions_by_id(bpe.exercise.id)
                except BodyPartExercise.DoesNotExist:
                    summary_data = None
            return render(request, 'edit_session.html', {'form': form, 'errors': form.errors, 'summary_data': summary_data})
    else:
        form = WorkoutSessionForm()
        summary_data = get_all_workout_sessions_by_id(bpe.exercise.id)
        return render(request, 'edit_session.html', {'form': form, 'summary_data': summary_data})

def get_suggestions_api_workout(request):
    if request.method == 'POST':
        body_part = request.POST.get('body_part', '')
        if body_part:
            suggestion = get_suggestions_for_exercise(body_part)
            return JsonResponse({'suggestion': suggestion})
        else:
            return JsonResponse({'error': 'Body part is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
