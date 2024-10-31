from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>', views.RoomDetail.as_view(), name='room-detail'), 
    path('generate-image/', views.GenerateImageView.as_view(), name='generate_image'),  # Use .as_view() here
    path('recommendations/', views.RoomRecommendationView.as_view(), name='room-recommendations'),  # New endpoint

]
