from django.urls import path
from . import views

urlpatterns = [
    path('quiz', views.quiz_list, name='quiz_list'),
    path('quiz/<int:Quizid>', views.singlequiz, name='singlequiz'),
    path('question', views.question_list, name='question_list'),
]
