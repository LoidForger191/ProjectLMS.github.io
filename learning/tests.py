from django.test import TestCase
from django.urls import reverse

from .models import (
    Assignment,
    Category,
    Course,
    Enrollment,
    Lesson,
    LessonProgress,
    Quiz,
    QuizAttempt,
    QuizQuestion,
    Submission,
    User,
)


class LearningFlowTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher", password="Teaching-12345", role=User.Role.TEACHER
        )
        self.student = User.objects.create_user(
            username="student", password="Learning-12345", role=User.Role.STUDENT
        )
        self.category = Category.objects.create(name="Design")
        self.course = Course.objects.create(
            title="Thoughtful Design",
            summary="Learn design by doing.",
            description="A practical course.",
            category=self.category,
            instructor=self.teacher,
            is_published=True,
        )
        self.lesson = Lesson.objects.create(
            course=self.course, title="Start here", content="Welcome to the course.", position=1
        )
        self.assignment = Assignment.objects.create(
            course=self.course, title="First reflection", instructions="Write a short response."
        )
        self.quiz = Quiz.objects.create(course=self.course, title="Getting started")
        self.question = QuizQuestion.objects.create(
            quiz=self.quiz,
            prompt="Which is the first letter?",
            option_a="A answer",
            option_b="B answer",
            option_c="C answer",
            option_d="D answer",
            correct_choice=QuizQuestion.Choice.A,
        )

    def test_registration_creates_a_student(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-learner",
                "first_name": "New",
                "last_name": "Learner",
                "email": "new@example.com",
                "password1": "A-safe-password-384!",
                "password2": "A-safe-password-384!",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="new-learner")
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertTrue(user.is_authenticated)

    def test_student_must_enroll_before_opening_course_material(self):
        self.client.force_login(self.student)
        self.assertEqual(
            self.client.get(reverse("lesson_detail", args=[self.lesson.id])).status_code, 403
        )
        self.client.post(reverse("enroll", args=[self.course.slug]))
        self.assertTrue(
            Enrollment.objects.filter(student=self.student, course=self.course).exists()
        )
        response = self.client.get(reverse("lesson_detail", args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.client.post(reverse("lesson_complete", args=[self.lesson.id]))
        self.assertTrue(
            LessonProgress.objects.filter(
                enrollment__student=self.student, lesson=self.lesson
            ).exists()
        )
        self.assertContains(self.client.get(reverse("dashboard")), "100% complete")

    def test_student_can_submit_and_teacher_can_grade_assignment(self):
        self.client.force_login(self.student)
        self.client.post(reverse("enroll", args=[self.course.slug]))
        response = self.client.post(
            reverse("assignment_detail", args=[self.assignment.id]),
            {"response": "A considered response."},
        )
        self.assertRedirects(
            response, reverse("assignment_detail", args=[self.assignment.id])
        )
        submission = Submission.objects.get(assignment=self.assignment, student=self.student)

        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse("grade_submission", args=[submission.id]),
            {"grade": "92.50", "feedback": "Clear and thoughtful."},
        )
        self.assertRedirects(
            response, reverse("assignment_detail", args=[self.assignment.id])
        )
        submission.refresh_from_db()
        self.assertEqual(str(submission.grade), "92.50")
        self.assertEqual(submission.graded_by, self.teacher)
        self.assertIsNotNone(submission.graded_at)

    def test_grade_above_maximum_is_rejected(self):
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            response="A considered response.",
        )
        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse("grade_submission", args=[submission.id]),
            {"grade": "101", "feedback": "Out of range."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "grade", "Grade must be between 0 and 100.")
        submission.refresh_from_db()
        self.assertIsNone(submission.grade)

    def test_quiz_answers_are_scored_without_exposing_the_key(self):
        self.client.force_login(self.student)
        self.client.post(reverse("enroll", args=[self.course.slug]))
        page = self.client.get(reverse("quiz_detail", args=[self.quiz.id]))
        self.assertContains(page, "A answer")
        self.assertNotContains(page, "correct_choice")

        self.client.post(
            reverse("quiz_detail", args=[self.quiz.id]),
            {f"question_{self.question.id}": QuizQuestion.Choice.A},
        )
        attempt = QuizAttempt.objects.get(quiz=self.quiz, student=self.student)
        self.assertEqual(attempt.score, 1)
        self.assertEqual(attempt.total_questions, 1)
        self.assertEqual(attempt.percentage, 100)

    def test_teacher_cannot_manage_another_teachers_course(self):
        other_teacher = User.objects.create_user(
            username="other", password="Teaching-12345", role=User.Role.TEACHER
        )
        self.client.force_login(other_teacher)
        response = self.client.get(reverse("course_edit", args=[self.course.slug]))
        self.assertEqual(response.status_code, 403)
