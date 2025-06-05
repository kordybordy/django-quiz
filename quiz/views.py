from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
import sqlite3
import random
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Track whether a test cookie was recently set so we can detect failure
_test_cookie_pending = False

DB_PATH = Path(settings.BASE_DIR) / 'pytania_egzaminacyjne.db'
QUESTION_LIMIT = 150
QUIZ_DURATION_SECONDS = 150 * 60


def get_random_questions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rok, numer, tresc, odpowiedz_a, odpowiedz_b, odpowiedz_c, poprawna_odpowiedz, podstawa_prawna FROM pytania")
    all_questions = cursor.fetchall()
    conn.close()
    return random.sample(all_questions, min(QUESTION_LIMIT, len(all_questions)))


def index(request):
    """Set a test cookie and redirect to cookie check."""
    request.session.set_test_cookie()
    return redirect('check_cookie')


def check_cookie(request):
    """Verify that the browser accepted the test cookie before starting the quiz."""
    global _test_cookie_pending

    if not request.session.test_cookie_worked():
        logger.debug("Test cookie failed; cookies seem to be disabled.")
        request.session.delete_test_cookie()
        _test_cookie_pending = False
        return redirect('cookies_required')

    request.session.delete_test_cookie()
    _test_cookie_pending = False

    # Ciasteczka działają – utwórz quiz
    questions = get_random_questions()
    request.session['quiz'] = {
        'questions': questions,
        'current': 0,
        'score': 0,
        'answers': [],
        'start_time': timezone.now().timestamp()
    }
    return redirect('quiz')


def quiz_view(request):
    global _test_cookie_pending
    quiz = request.session.get('quiz')
    if not quiz:
        if _test_cookie_pending and not request.session.test_cookie_worked():
            logger.debug("Test cookie failed; cookies seem to be disabled.")
            if request.session.get(request.session.TEST_COOKIE_NAME) is not None:
                request.session.delete_test_cookie()
            _test_cookie_pending = False
            return redirect('cookies_required')
        _test_cookie_pending = False
        return redirect('index')

    if _test_cookie_pending:
        if not request.session.test_cookie_worked():
            logger.debug(
                "Test cookie failed during quiz; redirecting to warning page.")
            request.session.delete_test_cookie()
            _test_cookie_pending = False
            return redirect('cookies_required')
        request.session.delete_test_cookie()
        _test_cookie_pending = False

    elapsed = timezone.now().timestamp() - quiz['start_time']
    remaining = QUIZ_DURATION_SECONDS - elapsed

    if remaining <= 0 or quiz['current'] >= len(quiz['questions']):
        return redirect('result')

    q = quiz['questions'][quiz['current']]
    correct = (q[6] or '').strip().upper()

    if request.method == 'POST':
        if request.POST.get('action') == 'skip':
            quiz['questions'].append(quiz['questions'].pop(quiz['current']))
            request.session['quiz'] = quiz
            return redirect('quiz')

        answer = request.POST.get('answer', '')
        result = 'correct' if answer == correct else 'wrong'
        if result == 'correct':
            quiz['score'] += 1
        quiz['answers'].append((q, answer, correct))
        quiz['current'] += 1
        request.session['quiz'] = quiz
        return redirect(f"{reverse('quiz')}?result={result}")

    minutes = int(remaining // 60)
    seconds = int(remaining % 60)

    return render(request, 'quiz/index.html', {
        'question_number': quiz['current'] + 1,
        'total_questions': len(quiz['questions']),
        'question': q,
        'time_remaining': f"{minutes:02d}:{seconds:02d}"
    })


def result_view(request):
    quiz = request.session.get('quiz')
    if not quiz:
        return redirect('index')

    score = quiz['score']
    total = len(quiz['questions'])
    request.session.pop('quiz', None)

    return render(request, 'quiz/result.html', {
        'score': score,
        'total': total
    })


def cookies_required(request):
    """Display a message that cookies must be enabled."""
    return render(request, 'quiz/cookies_required.html')
