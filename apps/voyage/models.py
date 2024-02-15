"""
Voyage Model
"""

from datetime import timedelta
import random
from django.contrib.auth import get_user_model
from django.db import models
# import git
from qux.models import QuxModel
from faker import Faker


class Faculty(QuxModel):
    """
    Faculty Model
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        fake = Faker()
        faculties = []
        for _ in range(5):
            user = get_user_model().objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            faculty = Faculty(
                user=user,
                github=fake.user_name(),
                is_active=random.choice([True, False]),
            )
            faculties.append(faculty)
        Faculty.objects.bulk_create(faculties)

    def programs(self):
        """
        returns all programs associated with this faculty.
        """
        return Program.objects.filter(assignment__content__faculty=self).distinct()

    def courses(self):
        """
        returns all courses associated with programs of this faculty.
        """

        return Course.objects.filter(assignment__content__faculty=self).distinct()

    def content(self, program=None, course=None):
        """
        returns content associated with programs or courses of this faculty.
        """

        if program and course:
            return self.content_set.filter(
                assignment__program=program, assignment_course=course
            ).distinct()
        if program:
            return self.content_set.filter(assignment__program=program).distinct()
        if course:
            return self.content_set.filter(assignment_course=course).distinct()

        return self.content_set.all().distinct()

    def num_assignments(self):
        """
        number of assignments created by each faculty.
        """
        return Assignment.objects.filter(content__faculty=self).distinct()

    def assignments_graded(self, assignment=None):
        """
        returns graded assignments associated with this faculty.
        """
        if assignment:
            return self.studentassignment_set.filter(
                grade__isnull=False, assignment=assignment
            ).count()
        return self.studentassignment_set.filter(grade__isnull=False)


class Program(QuxModel):
    """
    Example: Cohort-2
    """

    name = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        fake = Faker()
        program_names = [
            "Cohort-1",
            "Cohort-2",
            "Cohort-3",
            "Cohort-4",
            "Cohort-5",
            "Cohort-6",
            "Cohort-7",
            "Cohort-8",
            "Cohort-9",
            "Cohort-10",
        ]
        for program_name in program_names:
            start_date = fake.date_time_between(start_date="-1y", end_date="now")
            duration = fake.random_int(min=1, max=12)
            end_date = start_date + timedelta(days=duration * 30)

            Program.objects.create(
                name=program_name,
                start=start_date,
                end=end_date,
            )

    def __str__(self):
        """
        display
        """
        return f"{self.name}"

    def students(self):
        """
        number of students in each program.
        """
        return self.student_set.all()

    def courses(self):
        """
        number of courses in each program.
        """
        return Course.objects.filter(assignment__program=self).distinct()


class Course(QuxModel):
    """
    Example: Python, or Django, or Logic
    """

    name = models.CharField(max_length=128, unique=True)

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        course_names = [
            "Python",
            "Django",
            "Logic",
            "HTML",
            "CSS",
            "JavaScript",
            "Java",
            "MySQL",
            "React",
            "Angular",
        ]
        for _ in range(3):
            course_name = random.choice(course_names)
            Course.objects.create(name=course_name)

    def __str__(self):
        """
        display
        """
        return f"{self.name}"

    def programs(self):
        """
        returns programs associated with this course
        """
        return Program.objects.filter(assignment__course=self)

    @property
    def students(self):
        """
        returns students associated with this course
        """
        return Student.objects.filter(program__assignment__course=self).distinct()

    def content(self):
        """
        return content associated with this course
        """
        return Content.objects.filter(assignment__course=self).distinct()

    @property
    def assignments(self):
        """
        returns assignments associated with this course
        """
        return self.assignment_set.all()

    def completed_assignments(self):
        """
        number of assignments that are completed and graded 100%
        """
        return StudentAssignment.objects.filter(assignment__course=self).distinct()


class Content(QuxModel):
    """
    Meta information related to a GitHub repo
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class Meta:
        """
        Meta class
        """

        verbose_name = "Content"
        verbose_name_plural = "Content"

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        fake = Faker()
        faculties = Faculty.objects.all()
        contents = []
        for _ in range(28):
            faculty = random.choice(faculties)
            name = fake.catch_phrase()
            repo = fake.uri()

            content = Content(name=name, faculty=faculty, repo=repo)
            contents.append(content)
        Content.objects.bulk_create(contents)

    def courses(self):
        """
        return number of courses
        """
        return Course.objects.filter(assignment__content=self).distinct()

    def assignments(self):
        """
        assignments that use each content.
        """
        return self.assignment_set.all()


class Student(QuxModel):
    """
    Student Model
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        fake = Faker()
        programs = Program.objects.all()
        students = []
        for _ in range(10):
            user = get_user_model().objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            github_username = fake.user_name()
            program = random.choice(programs)
            student = Student(
                user=user, github=github_username, program=program, is_active=True
            )
            students.append(student)
        Student.objects.bulk_create(students)

    def courses(self):
        """
        return courses associated with this student's program
        """
        return Course.objects.filter(assignment__program__student=self).distinct()

    def assignments(self):
        """
        return assignments
        """
        studentassignments = self.studentassignment_set.all().distinct()
        return [assignment.assignment for assignment in studentassignments]

    def assignments_submitted(self, assignment=None):
        """
        returnS submitted assignments
        """
        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=False
            )
        return self.studentassignment_set.filter(submitted__isnull=False)

    def assignments_not_submited(self, assignment=None):
        """
        returns assignments not submitted
        """
        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=True
            )
        return self.studentassignment_set.filter(submitted__isnull=True)

    def assignments_graded(self, assignment=None):
        """
        returns graded assignments
        """
        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=False, grade__isnull=False
            )
        return self.studentassignment_set.filter(
            submitted__isnull=False, grade__isnull=False
        )

    def average_grade(self):
        """
        average grade of each student.
        """
        submitted_assignments = self.studentassignment_set.filter(
            submitted__isnull=False
        )
        total_assignments = self.studentassignment_set.all().count()
        total_grade = sum(assignment.grade for assignment in submitted_assignments)
        return round(total_grade / total_assignments, 2)

    def get_grade(self, assignments):
        """
        return the grade of all the assignments of a student
        """
        assignment_grade = {}
        for assignment in assignments:
            assignmentgrade = StudentAssignment.objects.filter(
                student=self, assignment=assignment
            )
            total_grade = sum(assignment.grade for assignment in assignmentgrade)
            assignment_grade[assignment] = round(total_grade / len(assignmentgrade), 2)
        return assignment_grade

    def find_total_submissions(self, assignments):
        """
        return the total number of submissions of each assignment
        """
        submitted_assignments = {}
        for assignment in assignments:
            total_submissions = len(
                StudentAssignment.objects.filter(
                    assignment=assignment.assignment, student=self
                )
            )
            submitted_assignments[assignment.assignment] = total_submissions
        return submitted_assignments


class Assignment(QuxModel):
    """
    Assignment Model
    """

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()

    class Meta:
        """
        Meta class
        """

        unique_together = ["program", "course", "content"]

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        fake = Faker()
        programs = Program.objects.all()
        courses = Course.objects.all()
        contents = Content.objects.all()

        for _ in range(5):
            program = random.choice(programs)
            course = random.choice(courses)
            content = random.choice(contents)

            due_date = fake.date_time_between(start_date="now", end_date="+30d")

            instructions = fake.paragraph()
            rubric = fake.paragraph()

            Assignment.objects.create(
                program=program,
                course=course,
                content=content,
                due=due_date,
                instructions=instructions,
                rubric=rubric,
            )

    def __str__(self):
        return self.content.name

    def students(self):
        """
        return students
        """
        Student.objects.filter(studentassignment__assignment=self).distinct()

    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        if graded:
            return self.studentassignment_set.filter(grade__isnull=False)
        if not graded:
            return self.studentassignment_set.filter(grade__isnull=True)
        return self.studentassignment_set.all()

    def avg_grade(self):
        """
        average grade of each assignment.
        """
        submissions = self.studentassignment_set.filter(grade__isnull=False)
        assignments = self.studentassignment_set.all().count()
        total_grade = sum(submission.grade for submission in submissions)
        return round(total_grade / assignments, 2)

    # def clone_repo_for_student(self, course_repo_url, student_username):
    #     repo = git.Repo.clone_from(
    #         course_repo_url,
    #         f"https://github.com/{student_username}/{self.content.name}",
    #     )
    #     return repo

    # def save(self, **kwargs):
    #     students = Student.objects.all()
    #     for student in students:
    #         self.clone_repo_for_student(self.content.repo, student.user.username)

    #     return super().save(**kwargs)


class StudentAssignment(QuxModel):
    """
    StudentAssignment Model
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=None,
        null=True,
        blank=True,
    )
    submitted = models.DateTimeField(default=None, null=True, blank=True)
    reviewed = models.DateTimeField(default=None, null=True, blank=True)
    reviewer = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, default=None, null=True, blank=True
    )
    feedback = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        """
        display
        """
        return f"{self.student} - {self.assignment}"

    @classmethod
    def generate_random_data(cls):
        """
        generating random data
        """
        fake = Faker()
        students = Student.objects.all()
        assignments = Assignment.objects.all()
        faculties = Faculty.objects.all()

        student_assignments = []
        for _ in range(45):
            student = random.choice(students)
            assignment = random.choice(assignments)
            grade = round(random.uniform(0, 100), 2)
            submitted_date = fake.date_time_between(start_date="-30d", end_date="now")
            reviewed_date = fake.date_time_between(start_date="-30d", end_date="now")
            reviewer = random.choice(faculties)
            feedback = fake.paragraph()

            student_assignment = StudentAssignment(
                student=student,
                assignment=assignment,
                grade=grade,
                submitted=submitted_date,
                reviewed=reviewed_date,
                reviewer=reviewer,
                feedback=feedback,
            )
            student_assignments.append(student_assignment)
        StudentAssignment.objects.bulk_create(student_assignments)
