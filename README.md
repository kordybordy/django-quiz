# Django Quiz Application

This project contains a small Django application that serves a multiple-choice quiz.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
The app uses cookie-based sessions, so you don't need to apply migrations.
Cookies must be enabled in the browser. If the test cookie set during
initialization isn't returned, the application redirects to a page informing
that cookies are required. This error page is served from `/cookies-required/`.
2. Run the development server:
   ```bash
    python manage.py runserver
    ```

The quiz interface also lets you skip a question. When you choose to skip,
the question is moved to the end of the list so you can answer it later.

The project's root URL configuration lives in `quiz_django/urls.py`.

## Running tests

Execute Django's test suite with:

```bash
python manage.py test
```

The quiz questions are loaded from the bundled SQLite database `pytania_egzaminacyjne.db`.
