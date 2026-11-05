from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    AssignmentForm,
    CourseForm,
    GradeForm,
    LessonForm,
    QuizForm,
    QuizQuestionForm,
    RegistrationForm,
    SubmissionForm,
)
from .models import (
    Assignment,
    Category,
    Course,
    Enrollment,
    Lesson,
    LessonProgress,
    Quiz,
    QuizAnswer,
    QuizAttempt,
    QuizQuestion,
    Submission,
    User,
)


def home(request):
    courses = Course.objects.filter(is_published=True).select_related("category", "instructor")[:6]
    return render(request, "learning/home.html", {"courses": courses})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


def course_catalog(request):
    courses = Course.objects.filter(is_published=True).select_related("category", "instructor")
    selected_category = request.GET.get("category", "")
    search = request.GET.get("q", "").strip()
    if selected_category:
        courses = courses.filter(category__slug=selected_category)
    if search:
        courses = courses.filter(title__icontains=search) | courses.filter(
            summary__icontains=search
        )
    return render(
        request,
        "learning/course_catalog.html",
        {
            "courses": courses.distinct(),
            "categories": Category.objects.all(),
            "selected_category": selected_category,
            "search": search,
        },
    )


def _can_manage_course(user, course):
    return user.is_lms_admin or (user.is_teacher and course.instructor_id == user.id)


def _can_access_course(user, course):
    return _can_manage_course(user, course) or (
        course.is_published and Enrollment.objects.filter(student=user, course=course).exists()
    )


def _require_teacher(request):
    if not request.user.is_authenticated:
        return None
    if not request.user.is_teacher and not request.user.is_lms_admin:
        return HttpResponseForbidden("Teacher access is required.")
    return None


def _managed_course_or_403(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not _can_manage_course(request.user, course):
        return None, HttpResponseForbidden("You cannot manage this course.")
    return course, None


@login_required
def dashboard(request):
    user = request.user
    if user.is_lms_admin:
        context = {
            "role": "Administrator",
            "course_count": Course.objects.count(),
            "student_count": User.objects.filter(role=User.Role.STUDENT).count(),
            "teacher_count": User.objects.filter(role=User.Role.TEACHER).count(),
            "enrollment_count": Enrollment.objects.count(),
            "recent_courses": Course.objects.select_related("instructor", "category")[:5],
        }
    elif user.is_teacher:
        courses = Course.objects.filter(instructor=user).prefetch_related("lessons")
        context = {
            "role": "Teacher",
            "courses": courses,
            "pending_submissions": Submission.objects.filter(
                assignment__course__instructor=user, grade__isnull=True
            ).select_related("assignment", "student", "assignment__course")[:8],
        }
    else:
        enrollments = Enrollment.objects.filter(student=user).select_related(
            "course", "course__category", "course__instructor"
        ).prefetch_related("lesson_progress", "course__lessons")
        for enrollment in enrollments:
            total = enrollment.course.lessons.count()
            enrollment.progress_percent = (
                round(enrollment.lesson_progress.count() * 100 / total) if total else 0
            )
        context = {
            "role": "Student",
            "enrollments": enrollments,
            "recent_attempts": QuizAttempt.objects.filter(student=user).select_related(
                "quiz", "quiz__course"
            )[:5],
            "recent_grades": Submission.objects.filter(
                student=user, grade__isnull=False
            ).select_related("assignment", "assignment__course")[:5],
        }
    return render(request, "learning/dashboard.html", context)


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.select_related("category", "instructor").prefetch_related(
            "lessons", "assignments", "quizzes"
        ),
        slug=slug,
    )
    can_manage = request.user.is_authenticated and _can_manage_course(request.user, course)
    enrolled = request.user.is_authenticated and Enrollment.objects.filter(
        student=request.user, course=course
    ).exists()
    if not course.is_published and not can_manage:
        return HttpResponseForbidden("This course is not available.")
    if request.user.is_authenticated:
        for lesson in course.lessons.all():
            lesson.is_completed = LessonProgress.objects.filter(
                enrollment__student=request.user, lesson=lesson
            ).exists()
    return render(
        request,
        "learning/course_detail.html",
        {
            "course": course,
            "can_manage": can_manage,
            "enrolled": enrolled,
            "assignments": course.assignments.all(),
            "quizzes": course.quizzes.all(),
        },
    )


@login_required
def course_create(request):
    denied = _require_teacher(request)
    if denied:
        return denied
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        course = form.save(commit=False)
        course.instructor = request.user
        course.save()
        messages.success(request, "Your course has been created.")
        return redirect("course_detail", slug=course.slug)
    return render(request, "learning/form_page.html", {"form": form, "title": "Create a course"})


@login_required
def course_edit(request, slug):
    course, denied = _managed_course_or_403(request, slug)
    if denied:
        return denied
    form = CourseForm(request.POST or None, instance=course)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Course details saved.")
        return redirect("course_detail", slug=course.slug)
    return render(request, "learning/form_page.html", {"form": form, "title": "Edit course"})


@login_required
@require_POST
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if request.user.role != User.Role.STUDENT:
        return HttpResponseForbidden("Only students can enroll in courses.")
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"You are enrolled in {course.title}.")
    return redirect("course_detail", slug=course.slug)


@login_required
def lesson_create(request, slug):
    course, denied = _managed_course_or_403(request, slug)
    if denied:
        return denied
    form = LessonForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        lesson = form.save(commit=False)
        lesson.course = course
        lesson.save()
        return redirect("course_detail", slug=course.slug)
    return render(
        request,
        "learning/form_page.html",
        {"form": form, "title": f"Add a lesson to {course.title}"},
    )


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related("course"), pk=lesson_id)
    if not _can_access_course(request.user, lesson.course):
        return HttpResponseForbidden("Enroll in this course to view its lessons.")
    enrollment = Enrollment.objects.filter(student=request.user, course=lesson.course).first()
    is_completed = bool(
        enrollment
        and LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).exists()
    )
    return render(
        request,
        "learning/lesson_detail.html",
        {"lesson": lesson, "enrollment": enrollment, "is_completed": is_completed},
    )


@login_required
@require_POST
def lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related("course"), pk=lesson_id)
    enrollment = get_object_or_404(
        Enrollment, student=request.user, course=lesson.course
    )
    LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    messages.success(request, "Lesson marked complete.")
    return redirect("lesson_detail", lesson_id=lesson.id)


@login_required
def assignment_create(request, slug):
    course, denied = _managed_course_or_403(request, slug)
    if denied:
        return denied
    form = AssignmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        assignment = form.save(commit=False)
        assignment.course = course
        assignment.save()
        return redirect("course_detail", slug=course.slug)
    return render(
        request,
        "learning/form_page.html",
        {"form": form, "title": f"Create an assignment for {course.title}"},
    )


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(
        Assignment.objects.select_related("course", "course__instructor"), pk=assignment_id
    )
    can_manage = _can_manage_course(request.user, assignment.course)
    enrollment = Enrollment.objects.filter(
        student=request.user, course=assignment.course
    ).first()
    if not can_manage and (not assignment.course.is_published or not enrollment):
        return HttpResponseForbidden("Enroll in this course to access assignments.")
    submission = None
    form = None
    if not can_manage:
        submission = Submission.objects.filter(
            assignment=assignment, student=request.user
        ).first()
        form = SubmissionForm(request.POST or None, instance=submission)
        if request.method == "POST" and form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.grade = None
            submission.feedback = ""
            submission.graded_by = None
            submission.graded_at = None
            submission.save()
            messages.success(request, "Your work has been submitted.")
            return redirect("assignment_detail", assignment_id=assignment.id)
    submissions = assignment.submissions.select_related("student") if can_manage else None
    return render(
        request,
        "learning/assignment_detail.html",
        {
            "assignment": assignment,
            "can_manage": can_manage,
            "submission": submission,
            "form": form,
            "submissions": submissions,
        },
    )


@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related(
            "assignment", "assignment__course", "student"
        ),
        pk=submission_id,
    )
    if not _can_manage_course(request.user, submission.assignment.course):
        return HttpResponseForbidden("You cannot grade submissions for this course.")
    form = GradeForm(request.POST or None, instance=submission)
    if request.method == "POST" and form.is_valid():
        submission = form.save(commit=False)
        submission.graded_by = request.user
        submission.graded_at = timezone.now()
        submission.save()
        messages.success(request, "Grade and feedback saved.")
        return redirect("assignment_detail", assignment_id=submission.assignment_id)
    return render(
        request,
        "learning/form_page.html",
        {"form": form, "title": f"Grade {submission.student.username}'s work"},
    )


@login_required
def quiz_create(request, slug):
    course, denied = _managed_course_or_403(request, slug)
    if denied:
        return denied
    form = QuizForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        quiz = form.save(commit=False)
        quiz.course = course
        quiz.save()
        return redirect("question_create", quiz_id=quiz.id)
    return render(
        request,
        "learning/form_page.html",
        {"form": form, "title": f"Create a quiz for {course.title}"},
    )


@login_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.select_related("course"), pk=quiz_id)
    if not _can_manage_course(request.user, quiz.course):
        return HttpResponseForbidden("You cannot edit this quiz.")
    form = QuizQuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        if "add_another" in request.POST:
            return redirect("question_create", quiz_id=quiz.id)
        return redirect("quiz_detail", quiz_id=quiz.id)
    return render(
        request,
        "learning/form_page.html",
        {"form": form, "title": f"Add a question to {quiz.title}", "add_another": True},
    )


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(
        Quiz.objects.select_related("course").prefetch_related("questions"), pk=quiz_id
    )
    can_manage = _can_manage_course(request.user, quiz.course)
    if not can_manage and (
        not quiz.course.is_published
        or not Enrollment.objects.filter(student=request.user, course=quiz.course).exists()
    ):
        return HttpResponseForbidden("Enroll in this course to take its quizzes.")
    questions = list(quiz.questions.all())
    for question in questions:
        question.options = [
            ("A", question.option_a),
            ("B", question.option_b),
            ("C", question.option_c),
            ("D", question.option_d),
        ]
    if request.method == "POST":
        if can_manage or request.user.role != User.Role.STUDENT:
            return HttpResponseForbidden("Only enrolled students can submit quiz answers.")
        if not questions:
            messages.error(request, "This quiz does not have any questions yet.")
            return redirect("quiz_detail", quiz_id=quiz.id)
        selections = {}
        for question in questions:
            selected = request.POST.get(f"question_{question.id}", "")
            if selected and selected not in QuizQuestion.Choice.values:
                messages.error(request, "One or more answers were invalid.")
                return redirect("quiz_detail", quiz_id=quiz.id)
            selections[question.id] = selected
        with transaction.atomic():
            attempt = QuizAttempt.objects.create(
                quiz=quiz, student=request.user, total_questions=len(questions)
            )
            answers = []
            for question in questions:
                selected = selections[question.id]
                if selected:
                    is_correct = selected == question.correct_choice
                    answers.append(
                        QuizAnswer(
                            attempt=attempt,
                            question=question,
                            selected_choice=selected,
                            is_correct=is_correct,
                        )
                    )
                    attempt.score += int(is_correct)
            QuizAnswer.objects.bulk_create(answers)
            attempt.save(update_fields=["score"])
        messages.success(
            request, f"You scored {attempt.score} out of {attempt.total_questions}."
        )
        return redirect("quiz_detail", quiz_id=quiz.id)
    attempts = (
        QuizAttempt.objects.filter(quiz=quiz, student=request.user)
        if not can_manage
        else QuizAttempt.objects.none()
    )
    return render(
        request,
        "learning/quiz_detail.html",
        {
            "quiz": quiz,
            "questions": questions,
            "can_manage": can_manage,
            "attempts": attempts,
        },
    )


@login_required
def grades(request):
    if request.user.is_lms_admin:
        submissions = Submission.objects.filter(grade__isnull=False)
        attempts = QuizAttempt.objects.all()
    elif request.user.is_teacher:
        submissions = Submission.objects.filter(
            assignment__course__instructor=request.user, grade__isnull=False
        )
        attempts = QuizAttempt.objects.filter(quiz__course__instructor=request.user)
    else:
        submissions = Submission.objects.filter(student=request.user, grade__isnull=False)
        attempts = QuizAttempt.objects.filter(student=request.user)
    return render(
        request,
        "learning/grades.html",
        {
            "submissions": submissions.select_related("assignment", "assignment__course", "student"),
            "attempts": attempts.select_related("quiz", "quiz__course", "student"),
        },
    )
