from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Art, Comment
from .serializers import ArtSerializer, CommentSerializer

# Create Art
@api_view(['POST'])
def create_art(request):
    serializer = ArtSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save without user since it's static for now
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Read Art (List)
@api_view(['GET'])
def list_arts(request):
    arts = Art.objects.all()
    serializer = ArtSerializer(arts, many=True)
    return Response(serializer.data)

# Read Art (Detail)
@api_view(['GET'])
def detail_art(request, art_id):
    try:
        art = Art.objects.get(id=art_id)
    except Art.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ArtSerializer(art)
    return Response(serializer.data)

# Update Art
@api_view(['PUT'])
def update_art(request, art_id):
    try:
        art = Art.objects.get(id=art_id)
    except Art.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ArtSerializer(art, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Art
@api_view(['DELETE'])
def delete_art(request, art_id):
    try:
        art = Art.objects.get(id=art_id)
        art.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Art.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Comment Functions
@api_view(['POST'])
def create_comment(request, art_id):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(art_id=art_id)  # Associate with the art piece
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_comments(request, art_id):
    comments = Comment.objects.filter(art_id=art_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# Delete Comment
@api_view(['DELETE'])
def delete_comment(request, art_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, art_id=art_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
