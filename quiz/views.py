from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Count
from .models import Category, Question, Result


# ---------------- HOME / CATEGORY LIST ----------------
@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'quiz/home.html', {'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/home.html', {'categories': categories})


# ---------------- AUTH ----------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'quiz/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())

            # redirect user to intended page if exists
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'home')
    else:
        form = AuthenticationForm()

    return render(request, 'quiz/login.html', {'form': form})

# ---------------- QUIZ --------------
@login_required
def quiz(request, category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_answer:
                score += 1

        # save result
        Result.objects.create(
    user=request.user,
    category=category,
    score=score,
    total=total
)

        request.session['score'] = score
        request.session['total'] = total

        return redirect('result')

    return render(request, 'quiz/quiz_page.html', {
        'questions': questions,
        'category': category
    })




# ---------------- RESULT ----------------
@login_required
def result(request):
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)

    context = {
        'score': score,
        'total': total,
        'wrong': total - score
    }
    return render(request, 'quiz/result.html', context)

@login_required

def result_history(request):
    results = Result.objects.filter(user=request.user).order_by('-id')

    stats = results.aggregate(
        total_attempts=Count('id'),
        highest_score=Max('score'),
        avg_score=Avg('score')
    )

    return render(request, 'quiz/result_history.html', {
        'results': results,
        'stats': stats
    })

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def quiz_by_category(request, category_id):
    questions = Question.objects.filter(category_id=category_id)

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_answer:
                score += 1

        Result.objects.create(
            user=request.user,
            score=score,
            total=total
        )

        request.session['score'] = score
        request.session['total'] = total

        return redirect('result')

    return render(request, 'quiz/quiz_page.html', {
        'questions': questions
    })

from django.db.models import Max, Count

def leaderboard(request):
    leaders = (
        Result.objects
        .values('user__username')
        .annotate(
            max_score=Max('score'),
            attempts=Count('id')
        )
        .order_by('-max_score', 'attempts')[:10]
    )

    return render(request, 'quiz/leaderboard.html', {'leaders': leaders})