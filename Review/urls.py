from django.urls import path,include 
from .views import (
    CourseListCreate,
    CourseRetrieveUpdateDestroy,
    CourseReviewListCreate,
    CourseReviewRetrieveUpdateDestroy,
    reviews_by_course   
)

urlpatterns = [
    path('courses/', CourseListCreate.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroy.as_view(), name='course-detail'),
    path('reviews/', CourseReviewListCreate.as_view(), name='course-review-list-create'),
    path('reviews/<int:pk>/', CourseReviewRetrieveUpdateDestroy.as_view(), name='course-review-detail'),
    path('courses/<int:course_id>/reviews/', reviews_by_course, name='reviews_by_course'),

]
