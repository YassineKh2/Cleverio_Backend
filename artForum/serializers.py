
from rest_framework import serializers
from .models import Art, Comment

class ArtSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Art
        fields = ['id', 'title', 'description', 'image', 'created_at', 'updated_at', 'user']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'art', 'content', 'created_at', 'user']
