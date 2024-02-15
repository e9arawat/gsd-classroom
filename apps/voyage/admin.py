"""
Voyage admin
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Faculty,
    Content,
    Program,
    Course,
    Student,
    Assignment,
    StudentAssignment,
)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """
    Faculty
    """

    list_display = (
        "user",
        "github",
        "num_courses_taught",
        "num_assignments",
        "num_assignments_graded",
    )

    def num_courses_taught(self, obj):
        """
        number of courses taught by each faculty.
        """
        # courses = len(obj.courses())
        # if courses > 0:
        #     courses_url = reverse("admin:voyage_course_changelist")
        #     faculty_courses_url = f"{courses_url}?faculty__id__exact={obj.id}"
        #     return format_html('<a href="{}">{}</a>', faculty_courses_url, courses)
        # return courses

        # courses = obj.courses()
        # if courses:
        #     links = []
        #     for course in courses:
        #         url = reverse("admin:voyage_course_change", args=[course.id])
        #         links.append(f'<option> <a href="{url}">{course.name}</a> </option>')
        #     return format_html("\n".join(links))
        # return 0

        courses = obj.courses()
        unique_id = [course.id for course in courses]
        if courses:
            url = '<a href="/admin/voyage/course/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(courses)}</a>')
        return 0

    num_courses_taught.short_description = "Courses Taught"

    def num_assignments(self, obj):
        """
        number of assignments created by each faculty.
        """
        assignments = obj.num_assignments()
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/assignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_assignments.short_description = "Assignments Created"

    def num_assignments_graded(self, obj):
        """
        number of assignments graded by each faculty.
        """
        assignments = obj.assignments_graded()
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_assignments_graded.short_description = "Assignments Graded"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Student
    """

    list_display = (
        "user",
        "github",
        "program_name",
        "num_courses_enrolled",
        "num_assignments_assigned",
        "num_assignments_submitted",
        "average_grade",
    )

    def program_name(self, obj):
        """
        program each student is enrolled in.
        """
        program = obj.program
        program_id = program.id
        url = f"<a href=/admin/voyage/program/{program_id}/change/>{program}</a>"
        return format_html(url)

    program_name.short_description = "Program"

    def num_courses_enrolled(self, obj):
        """
        number of courses each student is enrolled in.
        """
        courses = obj.courses()
        unique_id = [course.id for course in courses]
        if courses:
            url = '<a href="/admin/voyage/course/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(courses)}')
        return 0

    num_courses_enrolled.short_description = "Courses Enrolled"

    def num_assignments_assigned(self, obj):
        """
        number of assignments assigned to each student.
        """
        assignments = obj.assignments()
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_assignments_assigned.short_description = "Assignments Assigned"

    def num_assignments_submitted(self, obj):
        """
        number of assignments submitted by each student.
        """
        assignments = obj.assignments_submitted()
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_assignments_submitted.short_description = "Assignments Submitted"

    def average_grade(self, obj):
        """
        average grade of each student.
        """
        return obj.average_grade()

    average_grade.short_description = "Average Grade"


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Content
    """

    list_display = ("name", "num_courses_used", "num_assignments_used")

    def num_courses_used(self, obj):
        """
        number of courses
        """
        courses = obj.courses()
        if courses is None:
            return 0
        unique_id = [course.id for course in courses]
        if courses:
            url = '<a href="/admin/voyage/course/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(courses)}</a>')
        return 0

    num_courses_used.short_description = "Courses Used"

    def num_assignments_used(self, obj):
        """
        assignments that use each content.
        """
        assignments = obj.assignments()
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/assignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_assignments_used.short_description = "Assignments Used"


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Program
    """

    list_display = ("name", "num_courses", "num_students")

    def num_courses(self, obj):
        """
        number of courses in each program.
        """
        courses = obj.courses()
        unique_id = [course.id for course in courses]
        if courses:
            url = '<a href="/admin/voyage/course/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(courses)}</a>')
        return 0

    num_courses.short_description = "Courses"

    def num_students(self, obj):
        """
        number of students in each program.
        """
        students = obj.students()
        unique_id = [student.id for student in students]
        if students:
            url = '<a href="/admin/voyage/student/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(students)}')
        return 0

    num_students.short_description = "Students"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Course
    """

    list_display = ("name", "num_assignments", "num_completed_assignments")

    def num_assignments(self, obj):
        """
        number of assignments in each course.
        """
        assignments = obj.assignments()
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/assignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_assignments.short_description = "Assignments"

    def num_completed_assignments(self, obj):
        """
        number of assignments that are completed and graded 100%
        """
        assignments = obj.completed_assignments()
        if assignments is None:
            return 0
        unique_id = [assignment.id for assignment in assignments]
        if assignments:
            url = '<a href="/admin/voyage/assignment/?id__in='
            for i in unique_id:
                url = "".join((url, f"{i},"))
            return format_html(url[:-1] + f'">{len(assignments)}')
        return 0

    num_completed_assignments.short_description = "Completed Assignments"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Assignment
    """

    list_display = (
        "id",
        "program",
        "course",
        "content",
        "due",
        "instructions",
        "rubric",
        "average_grade",
    )

    def average_grade(self, obj):
        """
        average grade of each assignment.
        """
        return obj.avg_grade()

    average_grade.short_description = "Average Grade"


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    """
    Student Assignment
    """

    list_display = (
        "id",
        "student_username",
        "assignment",
        "grade",
        "submitted",
        "reviewed",
        "reviewer_username",
    )

    def student_username(self, obj):
        """
        return student name
        """
        return obj.student.user

    student_username.short_description = "Student"

    def reviewer_username(self, obj):
        """
        return reviewer name
        """
        return obj.reviewer.user

    reviewer_username.short_description = "Reviewer"
