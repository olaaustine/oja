from django import forms
from .models import Exercise, BodyPart, BodyPartExercise, WorkoutSession
from workout.workout_service import get_exercise_by_name_and_body_part


class BodyPartForm(forms.ModelForm):
    """Form for creating and editing BodyPart instances."""
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = BodyPart
        fields = ['name', 'description']

class BodyPartExerciseForm(forms.ModelForm):
    # Add fields for creating a new Exercise
    exercise_name = forms.CharField(max_length=100, label='Exercise Name')
    exercise_description = forms.CharField(widget=forms.Textarea, label='Exercise Description', required=False)

    class Meta:
        model = BodyPartExercise
        fields = ['body_part']
        widgets = {
            'body_part': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        exercise_name = cleaned.get('exercise_name')
        body_part = cleaned.get('body_part')

        existing_exercise =get_exercise_by_name_and_body_part(body_part, exercise_name)
        if existing_exercise:
            self.add_error('exercise_name', f'{exercise_name} already exists for {body_part}.')

        return cleaned

    def save(self, commit=True):
        body_part_exercise = super().save(commit=False)
        # Create a new Exercise instance
        exercise = Exercise.objects.create(
            name=self.cleaned_data['exercise_name'],
            description=self.cleaned_data['exercise_description']
        )
        body_part_exercise.exercise = exercise
        if commit:
            body_part_exercise.save()
        return body_part_exercise

class WorkoutSessionForm(forms.ModelForm):
    """Form for creating and editing WorkoutSession instances, including related Exercise fields."""
    # Add fields from Exercise for editing
    exercise_name = forms.CharField(max_length=100, label='Exercise Name')
    exercise_description = forms.CharField(widget=forms.Textarea, label='Exercise Description')
    exercise_weights = forms.IntegerField(label='Weights')
    exercise_sets = forms.IntegerField(label='Sets')
    exercise_reps = forms.IntegerField(label='Reps')

    class Meta:
        model = WorkoutSession
        fields = ['body_part_exercise', 'exercise_name', 'exercise_description', 'exercise_weights', 'exercise_sets', 'exercise_reps']
        widgets = {
            'body_part_exercise': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If a body_part_exercise is selected, prefill the fields with its exercise data
        if 'body_part_exercise' in self.data:
            try:
                bpe_id = int(self.data.get('body_part_exercise'))
                bpe = BodyPartExercise.objects.get(pk=bpe_id)
                exercise = bpe.exercise
                self.fields['exercise_name'].initial = exercise.name
                self.fields['exercise_description'].initial = exercise.description
                self.fields['exercise_weights'].initial = exercise.weights
                self.fields['exercise_sets'].initial = exercise.sets
                self.fields['exercise_reps'].initial = exercise.reps
            except (ValueError, BodyPartExercise.DoesNotExist, Exercise.DoesNotExist):
                pass
        elif self.instance and self.instance.body_part_exercise_id:
            body_part_exercise = self.instance.body_part_exercise
            exercise = body_part_exercise.exercise
            self.fields['exercise_name'].initial = exercise.name
            self.fields['exercise_description'].initial = exercise.description
            self.fields['exercise_weights'].initial = exercise.weights
            self.fields['exercise_sets'].initial = exercise.sets
            self.fields['exercise_reps'].initial = exercise.reps

    def save(self, commit=True):
        workout_session = super().save(commit=False)
        # Update the exercise linked to the selected BodyPartExercise
        body_part_exercise = workout_session.body_part_exercise
        exercise = body_part_exercise.exercise
        exercise.weights = self.cleaned_data['exercise_weights']
        exercise.sets = self.cleaned_data['exercise_sets']
        exercise.reps = self.cleaned_data['exercise_reps']
        exercise.save()
        if commit:
            workout_session.save()
        return workout_session
