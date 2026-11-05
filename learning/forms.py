from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Assignment, Course, Lesson, Quiz, QuizQuestion, Submission, User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title", "summary", "description", "category", "is_published")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "summary": forms.TextInput(attrs={"maxlength": 240}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "content", "material_url", "position")
        widgets = {"content": forms.Textarea(attrs={"rows": 8})}


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ("title", "instructions", "due_at")
        widgets = {"due_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("response",)
        widgets = {"response": forms.Textarea(attrs={"rows": 8})}


class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("grade", "feedback")
        widgets = {
            "grade": forms.NumberInput(attrs={"min": 0, "max": 100, "step": "0.01"}),
            "feedback": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_grade(self):
        grade = self.cleaned_data["grade"]
        if grade < 0 or grade > 100:
            raise forms.ValidationError("Grade must be between 0 and 100.")
        return grade


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("title", "instructions")


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = (
            "prompt",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_choice",
            "position",
        )
