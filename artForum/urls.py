from django.urls import path
from . import views

urlpatterns = [
    path('arts/', views.list_arts, name='list_arts'),
    path('arts/create/', views.create_art, name='create_art'),
    path('arts/<int:art_id>/', views.detail_art, name='detail_art'),
    path('arts/<int:art_id>/update/', views.update_art, name='update_art'),

    path('arts/<int:art_id>', views.delete_art, name='delete_art'),
    
     path('arts/<int:art_id>/comments/', views.list_comments, name='list_comments'),
    path('arts/<int:art_id>/comments/create/', views.create_comment, name='create_comment'),
    path('arts/<int:art_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
