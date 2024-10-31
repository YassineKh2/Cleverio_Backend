from django.urls import path
from .views import (
    get_all_persons,
    create_person,
    get_person_detail,
    update_person,
    delete_person,
    login_view, 
    toggle_active_status,
    update_profile_picture, 
    update_password, 
    create_admin,
authenticate_with_face,
get_csrf_token
)

urlpatterns = [
    path('persons', get_all_persons, name='get-all-persons'),
    path('register', create_person, name='create-person'),
    path('addAdmin', create_admin, name='create-admin'),

    path('persons/<int:pk>', get_person_detail, name='get-person-detail'),
    path('persons/<int:pk>/update', update_person, name='update-person'),
    path('persons/<int:pk>/delete', delete_person, name='delete-person'),
    path('login', login_view, name='login'),
    path('persons/<int:pk>/toggle-active', toggle_active_status, name='toggle-active-status'),
    path('persons/<int:pk>/update-profile-picture', update_profile_picture, name='update_profile_picture'),
    path('persons/<int:pk>/update-password', update_password, name='update-password'),
    path('face-auth', authenticate_with_face, name='face_auth'),
     path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),

]
