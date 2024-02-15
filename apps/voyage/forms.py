"""
Forms
"""
from django import forms
from .models import Course, Assignment


class CourseForm(forms.ModelForm):
    """
    form to create new course
    """

    class Meta:
        """
        Meta Class
        """
        model = Course
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class AssignmentForm(forms.ModelForm):
    """
    Assignment Form
    """
    class Meta:
        """
        Meta class
        """
        model = Assignment
        fields = ["program", "course", "content", "due", "instructions", "rubric"]
        widgets = {
            "program": forms.Select(attrs={"class": "form-select"}),
            "course": forms.Select(attrs={"class": "form-select"}),
            "content": forms.Select(attrs={"class": "form-select"}),
            "due": forms.DateTimeInput(attrs={"class": "form-control", "type": "date"}),
            "instructions": forms.Textarea(attrs={"class": "form-control"}),
            "rubric": forms.Textarea(attrs={"class": "form-control"}),
        }
