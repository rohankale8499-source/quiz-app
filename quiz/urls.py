from django.urls import path
from . import views

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
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]