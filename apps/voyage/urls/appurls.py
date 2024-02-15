from django.urls import path

from ..views.appviews import VoyageDefaultView, FacultyDashboardView, StudentDashboardView, StudentAssignmentView, StudentSubmittedAssignmentsView, CreateNewCourse, CreateNewAssignment, StudentHomeview, FacultyHomeView

urlpatterns = [
    path("", VoyageDefaultView.as_view(), name="home"),
    path("home/faculty/", FacultyHomeView.as_view(), name='faculty_home'),
    path("home/student/", StudentHomeview.as_view(), name='student_home'),
    path('dashboard/faculty/<int:faculty_id>/', FacultyDashboardView.as_view(), name="faculty_dashboard"),
    path('dashboard/student/<int:student_id>/', StudentDashboardView.as_view(), name="student_dashboard"),
    path('student-assignments/<int:student_id>/', StudentAssignmentView.as_view(), name="student_assignment"),
    path('student-submitted-assignments/<int:student_id>/', StudentSubmittedAssignmentsView.as_view(), name="student_assignment"),
    path('course/new/', CreateNewCourse.as_view(), name='create_course'),
    path('assignment/new/', CreateNewAssignment.as_view(), name="create_assignment"),

]
