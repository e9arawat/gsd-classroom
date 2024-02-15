from typing import Any
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from apps.voyage.models import Faculty, Student
from django.core.exceptions import ObjectDoesNotExist
from ..forms import CourseForm, AssignmentForm

from qux.seo.mixin import SEOMixin


class VoyageDefaultView(SEOMixin, ListView):
    template_name = "voyage/index.html"

class FacultyHomeView(ListView):
    template_name = "voyage/home.html"
    model = Faculty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_of'] = "faculty"
        return context


class StudentHomeview(ListView):
    template_name = "voyage/home.html"
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_of'] = "student"
        return context

class FacultyDashboardView(ListView):
    model = Faculty
    template_name = "voyage/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty_id = self.kwargs['faculty_id']
        try:
            faculty = self.model.objects.get(id=faculty_id)
        except ObjectDoesNotExist:
            context['error_message'] = "Faculty Does not exist"
            return context
        context['courses'] = faculty.courses()
        context['designation'] = 'faculty'
        return context
    
class StudentDashboardView(ListView):
    model = Student
    template_name = "voyage/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        try:
            student = self.model.objects.get(id=student_id)
        except ObjectDoesNotExist:
            context['error_message'] = "Student Does not exist"
            return context
        context['courses'] = student.courses()
        context['student_id'] = student_id
        return context
    
class StudentAssignmentView(ListView):
    model = Student
    template_name = 'voyage/student-assignments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        try:
            student = self.model.objects.get(id=student_id)
        except ObjectDoesNotExist:
            context['error_message'] = "Student Does Not exist"
        
        assignments = student.assignments()
        context['headers'] = ['Assignments', 'Grade']
        context['assignments'] = student.get_grade(assignments)
        context['student_id'] = student_id
        return context

class StudentSubmittedAssignmentsView(ListView):
    model = Student
    template_name = 'voyage/student-assignments.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        try:
            student = self.model.objects.get(id=student_id)
        except ObjectDoesNotExist:
            context['error_message'] = "Student Does Not exist"

        submitted_assignments = student.assignments_submitted()
        context['headers'] = ['Assignments', 'No of Submissions']
        context['assignments'] = student.find_total_submissions(submitted_assignments)
        context['student_id'] = student_id
        return context
        

class CreateNewCourse(TemplateView):
    template_name = "voyage/creation-form.html"
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.POST or None)
        context['heading'] = 'Course'
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context['form']
        if form.is_valid():
            form.save()
            return redirect('faculty_home')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CreateNewAssignment(TemplateView):
    template_name = "voyage/creation-form.html"
    form_class = AssignmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.POST or None)
        context['heading'] = 'Assignment'
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context['form']
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('faculty_home'))
        else:
            return self.render_to_response(self.get_context_data(form=form))
