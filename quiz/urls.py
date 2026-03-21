from django.urls import path
from . import views
from django.views.generic import RedirectView


urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Quiz
    path('quiz/<int:category_id>/', views.quiz, name='quiz'),

    # Result
    path('result/', views.result, name='result'),
    path('results/', views.result_history, name='result_history'),

    # Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('logout/', views.user_logout, name='logout'),

]