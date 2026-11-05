from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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


@admin.register(User)
class LMSUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Learning platform", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Learning platform", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")

    def save_model(self, request, obj, form, change):
        if obj.role == User.Role.ADMIN:
            obj.is_staff = True
        super().save_model(request, obj, form, change)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "instructor", "is_published")
    list_filter = ("is_published", "category")
    search_fields = ("title", "instructor__username")


admin.site.register(
    (Category, Lesson, Enrollment, LessonProgress, Assignment, Submission, Quiz, QuizQuestion,
     QuizAttempt, QuizAnswer)
)
