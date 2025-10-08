from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from workout.models import Exercise, BodyPartExercise, WorkoutSession
from workout.forms import (
    BodyPartForm,
    WorkoutSessionForm,
    BodyPartExerciseForm,
    CustomUserCreationForm,
)
from workout.workout_service import (
    get_all_workout_sessions_by_id,
    get_suggestions_for_exercise,
)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView


class LandingPageView(TemplateView):
    """View for the landing page."""

    template_name = "landing.html"


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class BodyPartExerciseListTemplateView(ListView):
    """View to list all BodyPartExercise entries."""

    model = BodyPartExercise
    template_name = "body_part_exercise_list.html"
    context_object_name = "object_list"
    paginate_by = 5

    def get_queryset(self):
        return BodyPartExercise.objects.select_related(
            "exercise", "body_part"
        ).order_by("exercise__name")


def get_exercise_details(request, id: int) -> JsonResponse:
    """Get exercise details by BodyPartExercise ID"""
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


@api_view(["GET"])
def get_exercise(exercise_id: int) -> Response:
    sessions = get_all_workout_sessions_by_id(exercise_id)
    if sessions is None:
        return Response(
            {"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND
        )
    else:
        return Response({"sessions": sessions}, status=status.HTTP_200_OK)


def add_body_part(request) -> HttpResponse:
    """View to add a new BodyPart"""
    if request.method == "POST":
        form = BodyPartForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request, "create_body_part.html", {"form": form, "success": True}
            )
        else:
            return render(
                request, "create_body_part.html", {"form": form, "errors": form.errors}
            )
    else:
        form = BodyPartForm()
    return render(request, "create_body_part.html", {"form": form})


def add_body_part_exercise(request) -> HttpResponse:
    suggestion = None
    if request.method == "POST":
        form = BodyPartExerciseForm(request.POST)
        if form.is_valid():
            # check if exercise with same name exists
            bodypart_exercise = form.save()
            # Get workout suggestion for the selected body part
            body_part_name = bodypart_exercise.body_part.name
            suggestion = get_suggestions_for_exercise(body_part_name)
            return render(
                request,
                "create_body_part_exercise.html",
                {"form": form, "success": True, "suggestion": suggestion},
            )
        else:
            return render(
                request,
                "create_body_part_exercise.html",
                {"form": form, "errors": form.errors},
            )
    else:
        form = BodyPartExerciseForm()
    return render(request, "create_body_part_exercise.html", {"form": form})


def add_workout_session(request) -> HttpResponse:
    """View to add a new WorkoutSession along with editing related Exercise fields"""
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "create_session.html",
                {
                    "form": form,
                    "success": True,
                },
            )
        else:
            return render(
                request, "create_session.html", {"form": form, "errors": form.errors}
            )
    else:
        form = WorkoutSessionForm()
    return render(request, "create_session.html", {"form": form})


def edit_workout_session(request, id) -> HttpResponse:
    """View to edit an existing WorkoutSession along with related Exercise fields"""
    summary_data = None
    try:
        bpe = BodyPartExercise.objects.get(id=id)
    except BodyPartExercise.DoesNotExist:
        return render(
            request,
            "edit_session.html",
            {
                "form": None,
                "errors": "BodyPartExercise not found",
                "summary_data": None,
                "workout_session": None,
            },
        )

    if request.method == "POST":
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            workout_session = form.save()
            summary_data = get_all_workout_sessions_by_id(bpe.exercise.id)
            return render(
                request,
                "edit_session.html",
                {
                    "form": form,
                    "success": True,
                    "summary_data": summary_data,
                    "workout_session": workout_session,
                },
            )
        else:
            if id:
                try:
                    bpe = BodyPartExercise.objects.get(id=id)
                    summary_data = get_all_workout_sessions_by_id(bpe.exercise.id)
                except BodyPartExercise.DoesNotExist:
                    summary_data = None
            return render(
                request,
                "edit_session.html",
                {
                    "form": form,
                    "errors": form.errors,
                    "summary_data": summary_data,
                    "workout_session": None,
                },
            )
    else:
        form = WorkoutSessionForm()
        summary_data = get_all_workout_sessions_by_id(bpe.exercise.id)
        workout_session = (
            WorkoutSession.objects.filter(body_part_exercise=bpe)
            .order_by("-date")
            .first()
        )
        return render(
            request,
            "edit_session.html",
            {
                "form": form,
                "summary_data": summary_data,
                "workout_session": workout_session,
            },
        )


def get_suggestions_api_workout(request):
    if request.method == "POST":
        body_part = request.POST.get("body_part", "")
        if body_part:
            suggestion = get_suggestions_for_exercise(body_part)
            return JsonResponse({"suggestion": suggestion})
        else:
            return JsonResponse({"error": "Body part is required"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)
