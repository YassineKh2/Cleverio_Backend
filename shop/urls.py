from django.urls import path
from . import views
from .views import delete_purchase
from .views import generate_amazon_link
from .views import quiz_view
from .views import add_game_points  # Import the new function

urlpatterns = [
    path('game-categories', views.category_list, name='category_list'),
    path('game-categories/<int:category_id>', views.category_detail, name='category_detail'),
    path('game', views.game_list, name='game_list'),
    path('game/<int:game_id>', views.game_detail, name='game_detail'),
    path('game/purchase', views.purchase_game, name='purchase_game'),
    path('game/purchase/<int:user_id>', views.user_purchases, name='user_purchases'),
    path('game/purchases', views.all_users_purchases, name='all_users_purchases'),
    path('game/purchase/delete', delete_purchase, name='delete_purchase'),  # New delete path
    path('game/link', generate_amazon_link, name='generate_amazon_link'),
    path('game/quiz', quiz_view, name='quiz_view'),
    path('game/addpoints/<int:user_id>', add_game_points, name='add_game_points'),


]
