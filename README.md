# Northstar Learning

A responsive learning management system built with Django, Django Templates, HTML, CSS, and lightweight JavaScript. SQLite is the development database; no frontend framework or third-party Django package is required.

## Run locally

1. Install Python 3.10+ and create an environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Create the database and an administrator:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. Start the development server:

   ```powershell
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/`. Reset-password emails are printed to the runserver console in development.

## Roles and learning flows

- **Students** register through the site, browse published courses, enroll, complete lessons, submit assignments, take quizzes, and view grades and progress.
- **Teachers** are created or promoted by an administrator in `/admin/`. They can publish courses, add lessons and resources, create assignments and quizzes, and grade student submissions with feedback.
- **Administrators** use Django's built-in admin to manage users, categories, courses, and learning records. A Django superuser receives the administrator dashboard automatically.

Public registration always creates a student account. Role checks and enrollment checks are enforced server-side, in addition to the controls shown in templates.

## Project map

- `config/` — Django settings, root URLs, and WSGI entry point.
- `learning/models.py` — custom user/roles, courses, lessons, enrollments, progress, assignments, submissions, quizzes, and results.
- `learning/forms.py` — validated registration and learning-management forms.
- `learning/views.py` and `learning/urls.py` — dashboards and role-protected learning workflows.
- `learning/admin.py` — staff management for platform data.
- `templates/` — shared layout, dashboards, course pages, assessments, and authentication/password-reset screens.
- `static/learning/styles.css` — responsive visual design and the small navigation interaction.

Run the automated checks with `python manage.py check`, `python manage.py makemigrations --check --dry-run`, and `python manage.py test`.

## Deployment note

This application requires a Python-capable Django host; GitHub Pages only serves static files and cannot run its authentication or database-backed features. Set `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and `DJANGO_DEBUG=false` in production, use a durable production database, and configure a real email backend for password resets. `config/settings.py` uses SQLite and console email for local development.
