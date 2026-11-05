from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("grades/", views.grades, name="grades"),
    path("courses/", views.course_catalog, name="course_catalog"),
    path("courses/create/", views.course_create, name="course_create"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("courses/<slug:slug>/edit/", views.course_edit, name="course_edit"),
    path("courses/<slug:slug>/enroll/", views.enroll, name="enroll"),
    path("courses/<slug:slug>/lessons/create/", views.lesson_create, name="lesson_create"),
    path("lessons/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<int:lesson_id>/complete/", views.lesson_complete, name="lesson_complete"),
    path(
        "courses/<slug:slug>/assignments/create/",
        views.assignment_create,
        name="assignment_create",
    ),
    path("assignments/<int:assignment_id>/", views.assignment_detail, name="assignment_detail"),
    path("submissions/<int:submission_id>/grade/", views.grade_submission, name="grade_submission"),
    path("courses/<slug:slug>/quizzes/create/", views.quiz_create, name="quiz_create"),
    path("quizzes/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path("quizzes/<int:quiz_id>/questions/create/", views.question_create, name="question_create"),
]
