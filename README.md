# Django Quiz Application

This project contains a small Django application that serves a multiple-choice quiz.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
The app uses cookie-based sessions, so you don't need to apply migrations.
Cookies must be enabled in the browser. At startup the `index` view sets a test
cookie and redirects to `/check-cookie/` where the cookie is verified. If the
test cookie isn't returned, the application redirects to `/cookies-required/` to
inform the user that cookies must be enabled.
2. Run the development server:
   ```bash
    python manage.py runserver
    ```

The quiz interface also lets you skip a question. When you choose to skip,
the question is moved to the end of the list so you can answer it later.

The project's root URL configuration lives in `quiz_django/urls.py`.

Static files are served automatically when `DEBUG=True`. In production
you should run `collectstatic` and serve files from the directory defined by
`STATIC_ROOT` (defaults to `staticfiles/`). The HTML templates reference
a favicon hosted at <https://www.djangoproject.com/favicon.ico>.

## Running tests

Execute Django's test suite with:

```bash
python manage.py test
```

The quiz questions are loaded from the bundled SQLite database `pytania_egzaminacyjne.db`.
