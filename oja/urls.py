"""
URL configuration for oja project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from workout.views import (
    LandingPageView,
    add_body_part,
    add_workout_session,
    add_body_part_exercise,
    get_exercise_details,
    BodyPartExerciseListTemplateView,
    edit_workout_session,
    get_exercise,
    get_suggestions_api_workout
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Body parts
    path("body-parts/create/", add_body_part, name="create_body_part"),

    # BodyPartExercise
    path("body-parts-exercises/create/", add_body_part_exercise, name="create_body_part_exercise"),

    # Workout sessions
    path("workout-sessions/create/", add_workout_session, name="create_workout_session"),

    # Landing
    path('', LandingPageView.as_view(), name='landing'),

    # API endpoint for exercise details
    path('api/exercise/<id>/', get_exercise_details, name='exercise_details'),

    path('body-parts-exercises/list/', BodyPartExerciseListTemplateView.as_view(), name='body_parts_exercises_list'),

    path('workout-sessions/<id>/edit/', edit_workout_session, name='edit_workout_session'),

    path('api/workout-sessions-calc/<int:exercise_id>/', get_exercise, name='workout_sessions_calculations'),

    path('api/suggestions/', get_suggestions_api_workout, name='suggest_workout_api')
]
