from rest_framework import generics
from .models import Course, CourseReview
from .serializers import CourseSerializer, CourseReviewSerializer
from django.views.decorators.http import require_GET
from django.http import JsonResponse

class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseReviewListCreate(generics.ListCreateAPIView):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer

class CourseReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Course

@require_GET
def reviews_by_course(request, course_id):
    try:
        # Fetch the course by ID to ensure it exists
        course = Course.objects.get(id=course_id)
        
        # Fetch reviews related to the course, including user information
        reviews = course.reviews.select_related('user').values(
            'id', 
            'user__username', 
            'user__profile_picture',  # Assuming your User model has this field
            'rating', 
            'comment'
        )

        # Create the response data
        response_data = {
            'course_id': course.id,
            'course_title': course.title,
            'reviews': list(reviews),  # Convert QuerySet to list
        }

        return JsonResponse(response_data, status=200)
    
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found.'}, status=404)
