from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        TEACHER = "teacher", "Teacher"
        STUDENT = "student", "Student"

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.STUDENT)

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER or self.is_superuser

    @property
    def is_lms_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="courses")
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "course"
            self.slug = base_slug
            suffix = 2
            while Course.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{suffix}"
                suffix += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=160)
    content = models.TextField()
    material_url = models.URLField(blank=True, help_text="Optional link to a resource or video.")
    position = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["position", "id"]
        constraints = [
            models.UniqueConstraint(fields=["course", "position"], name="unique_lesson_position")
        ]

    def __str__(self):
        return f"{self.course.title}: {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_course_enrollment")
        ]

    def __str__(self):
        return f"{self.student} — {self.course}"


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_records")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "lesson"], name="unique_lesson_completion"
            )
        ]


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=160)
    instructions = models.TextField()
    due_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_at", "created_at"]

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions"
    )
    response = models.TextField()
    submitted_at = models.DateTimeField(auto_now=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="graded_submissions",
    )
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"], name="unique_assignment_submission"
            )
        ]

    def __str__(self):
        return f"{self.assignment.title} — {self.student}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=160)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    class Choice(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    prompt = models.CharField(max_length=500)
    option_a = models.CharField(max_length=250)
    option_b = models.CharField(max_length=250)
    option_c = models.CharField(max_length=250)
    option_d = models.CharField(max_length=250)
    correct_choice = models.CharField(max_length=1, choices=Choice.choices)
    position = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.prompt


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts"
    )
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]

    @property
    def percentage(self):
        if not self.total_questions:
            return 0
        return round(self.score * 100 / self.total_questions)

    def __str__(self):
        return f"{self.quiz.title}: {self.student} ({self.percentage}%)"


class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    selected_choice = models.CharField(max_length=1, choices=QuizQuestion.Choice.choices)
    is_correct = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["attempt", "question"], name="unique_quiz_answer")
        ]
