from django.urls import path
from .views import (
    get_all_persons,
    create_person,
    get_person_detail,
    update_person,
    delete_person,
    login_view

)

urlpatterns = [
    path('persons', get_all_persons, name='get-all-persons'),
    path('register', create_person, name='create-person'),
    path('persons/<int:pk>', get_person_detail, name='get-person-detail'),
    path('persons/<int:pk>/update', update_person, name='update-person'),
    path('persons/<int:pk>/delete', delete_person, name='delete-person'),
    path('login', login_view, name='login'),
]
