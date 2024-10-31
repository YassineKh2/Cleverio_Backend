from rest_framework import serializers
from .models import Course, CourseReview

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # You can specify fields like ['id', 'title', 'description'] if needed
class CourseReviewSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CourseReview
        fields = ['id','course', 'course_title','user', 'username', 'rating', 'comment', 'created_at']

