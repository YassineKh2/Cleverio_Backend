from django.urls import path
from . import views

urlpatterns = [
    path('game-categories', views.category_list, name='category_list'),
    path('game-categories/<int:category_id>', views.category_detail, name='category_detail'),
    path('game', views.game_list, name='game_list'),
    path('game/<int:game_id>', views.game_detail, name='game_detail'),
]
