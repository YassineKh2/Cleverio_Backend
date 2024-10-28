from django.urls import path
from . import views

urlpatterns = [
    path('rooms', views.RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>', views.RoomDetail.as_view(), name='room-detail'), 
]
