from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import RoomSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image, UnidentifiedImageError  # Import UnidentifiedImageError
from django.conf import settings
import os
import io
import requests
import json
from rest_framework.permissions import AllowAny
import base64
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Constants for the image generation
IMAGEGEN_KEY = os.getenv("IMAGEGEN_KEY")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {IMAGEGEN_KEY}"}

def imageGen(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

class GenerateImageView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request):
        # Generate the image
        data = request.data  # Use request.data to handle JSON automatically
        title = data.get('title', '')

        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        print(title)
        
        image_bytes = imageGen({"inputs": title})  # Assuming imageGen returns base64 or raw bytes
            
        # Check if image_bytes is base64 string or raw bytes
        # Decode the base64 string
        image_bytes = base64.b64decode(image_bytes)
        print(image_bytes)

        # Now image_bytes should be in bytes format, try opening it with PIL
        image = Image.open(io.BytesIO(image_bytes))
        # This should now be reached if everything is working correctly

        # Ensure the media directory exists
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'), exist_ok=True)

        # Save the image temporarily to the filesystem (e.g., in the media directory)
        image_name = f'{title.replace(" ", "_")}_generated_image.jpg'
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)

        # Save the image to the file system
        with open(image_path, 'wb') as f:
            image.save(f, format='JPEG')  # Ensure this line is indented

        # Return the image URL
        return Response({'image_url': f'/media/images/{image_name}'}, status=status.HTTP_201_CREATED)

      



class RoomList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        # Fetch all rooms
        rooms = Room.objects.all()
        room_serializer = RoomSerializer(rooms, many=True, context={'request': request})

        # Get user's added rooms based on the authenticated user
        user = request.user  # Assuming the user is authenticated
        user_rooms = Room.objects.filter(createdBy=user.id)  # Adjust according to your User model
        recommended_room_ids = self.get_recommendations(user_rooms) if user_rooms.exists() else []

        recommended_rooms = Room.objects.filter(id__in=recommended_room_ids)
        recommended_serializer = RoomSerializer(recommended_rooms, many=True, context={'request': request})

        # Combine rooms and recommended rooms in the response data
        response_data = {
            'rooms': room_serializer.data,
            'recommended_rooms': recommended_serializer.data
        }

        return Response(response_data)

    def get_recommendations(self, user_rooms):
        if not user_rooms:
            return []

        all_rooms = Room.objects.all()

        # Create DataFrame for similarity calculations
        room_data = [{'id': r.id, 'description': r.description, 'subject': r.subject} for r in all_rooms]
        df = pd.DataFrame(room_data)

        # Combine descriptions and subjects for TF-IDF
        df['combined'] = df['description'] + " " + df['subject']

        # Calculate TF-IDF and cosine similarity
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Collect indices of the user's rooms
        user_room_ids = [room.id for room in user_rooms]
        recommended_room_ids = set()

        for user_room in user_rooms:
            idx = df.index[df['id'] == user_room.id].tolist()[0]
            sim_scores = list(enumerate(cosine_sim[idx]))

            # Exclude the room itself and sort scores
            sim_scores = [score for score in sim_scores if df.iloc[score[0]]['id'] != user_room.id]
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:5]  # Top 5 recommendations

            # Get the IDs of the top recommended rooms
            recommended_room_ids.update(df.iloc[score[0]]['id'] for score in sim_scores)

        return list(recommended_room_ids)
    def post(self, request):
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RoomDetail(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomRecommendationView(APIView):
    permission_classes = [AllowAny]  # Require authentication

    def get(self, request):
        user = request.user  # Get the logged-in user
        print(usr)
        recommended_room_ids = self.recommend_rooms(user)

        # Fetch the recommended room objects
        recommended_rooms = Room.objects.filter(id__in=recommended_room_ids)

        # Serialize the recommended rooms for response
        serializer = RoomSerializer(recommended_rooms, many=True, context={'request': request})
        return Response(serializer.data)

    def recommend_rooms(self, user):
    # Get all rooms for recommendation calculations
        all_rooms = Room.objects.all()

    # Get the rooms created by the user
        user_rooms = all_rooms.filter(createdBy=user)

        if not user_rooms.exists():
            return []  # Return an empty list if the user has no rooms

    # Gather descriptions and subjects for all rooms
        room_data = []
        for room in all_rooms:
            room_data.append({'id': room.id, 'description': room.description, 'subject': room.subject})

    # Create a DataFrame for all rooms
        df = pd.DataFrame(room_data)

    # Combine the description and subject for TF-IDF
        df['combined'] = df['description'] + " " + df['subject']

    # Compute TF-IDF vectors for all rooms
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined'])

    # Calculate cosine similarity for all rooms
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Collect recommendations by iterating over each user room
        recommendations = []
        user_room_ids = user_rooms.values_list('id', flat=True)
        for idx, row in df.iterrows():
            if row['id'] in user_room_ids:
            # Find similar rooms for each of the user's rooms
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Exclude the room itself and user's rooms
                sim_scores = [
                    score for score in sim_scores[1:]
                    if df.iloc[score[0]]['id'] not in user_room_ids
                ]

            # Get the top 5 similar rooms not created by the user
                for score in sim_scores[:5]:
                    recommended_room_id = df.iloc[score[0]]['id']
                    recommendations.append({'room_id': recommended_room_id, 'similarity': score[1]})

    # Get unique recommended rooms
        recommended_rooms = pd.DataFrame(recommendations).drop_duplicates('room_id')

    # Return the unique recommended room IDs
        return recommended_rooms['room_id'].tolist()
