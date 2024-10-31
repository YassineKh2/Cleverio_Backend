from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import RoomSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image, UnidentifiedImageError
from django.conf import settings
import os
import io
import requests
import base64
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Constants for the image generation
IMAGEGEN_KEY = os.getenv("IMAGEGEN_KEY")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {IMAGEGEN_KEY}"}

def imageGen(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

class GenerateImageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        title = data.get('title', '')

        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        image_bytes = imageGen({"inputs": title})
        image_bytes = base64.b64decode(image_bytes)

        try:
            image = Image.open(io.BytesIO(image_bytes))
        except UnidentifiedImageError:
            return Response({'error': 'Invalid image data'}, status=status.HTTP_400_BAD_REQUEST)

        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'), exist_ok=True)
        image_name = f'{title.replace(" ", "_")}_generated_image.jpg'
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)

        image.save(image_path, format='JPEG')

        return Response({'image_url': f'/media/images/{image_name}'}, status=status.HTTP_201_CREATED)
@method_decorator(csrf_exempt, name='dispatch')
class RoomList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        rooms = Room.objects.all()
        room_serializer = RoomSerializer(rooms, many=True, context={'request': request})

        user_id = request.headers.get("X-User-Id")
        user_rooms = Room.objects.filter(createdBy=user_id)
        recommended_room_ids = self.get_recommendations(user_rooms) if user_rooms.exists() else []

        recommended_rooms = Room.objects.filter(id__in=recommended_room_ids)
        recommended_serializer = RoomSerializer(recommended_rooms, many=True, context={'request': request})

        response_data = {
            'rooms': room_serializer.data,
            'recommended_rooms': recommended_serializer.data
        }

        return Response(response_data)

    def get_recommendations(self, user_rooms):
        if not user_rooms:
            return []

        all_rooms = Room.objects.all()
        room_data = [{'id': r.id, 'description': r.description, 'subject': r.subject} for r in all_rooms]
        df = pd.DataFrame(room_data)
        df['combined'] = df['description'] + " " + df['subject']

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        user_room_ids = [room.id for room in user_rooms]
        recommended_room_ids = set()

        for user_room in user_rooms:
            idx = df.index[df['id'] == user_room.id].tolist()[0]
            sim_scores = list(enumerate(cosine_sim[idx]))

            sim_scores = [
                score for score in sim_scores
                if df.iloc[score[0]]['id'] != user_room.id and score[1] > 0.1
            ]

            filtered_ids = [
                df.iloc[score[0]]['id'] for score in sim_scores
                if user_room.subject.lower() in df.iloc[score[0]]['subject'].lower()
                or user_room.description.lower() in df.iloc[score[0]]['description'].lower()
            ]
        
            recommended_room_ids.update(filtered_ids)

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
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        recommended_room_ids = self.recommend_rooms(user)

        recommended_rooms = Room.objects.filter(id__in=recommended_room_ids)
        serializer = RoomSerializer(recommended_rooms, many=True, context={'request': request})
        return Response(serializer.data)

    def recommend_rooms(self, user):
        all_rooms = Room.objects.all()
        user_rooms = all_rooms.filter(createdBy=user)

        if not user_rooms.exists():
            return []

        room_data = [{'id': room.id, 'description': room.description, 'subject': room.subject} for room in all_rooms]
        df = pd.DataFrame(room_data)
        df['combined'] = df['description'] + " " + df['subject']

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        recommendations = []
        user_room_ids = user_rooms.values_list('id', flat=True)

        for idx, row in df.iterrows():
            if row['id'] in user_room_ids:
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

                sim_scores = [
                    score for score in sim_scores[1:]
                    if df.iloc[score[0]]['id'] not in user_room_ids
                ]

                for score in sim_scores[:5]:
                    recommended_room_id = df.iloc[score[0]]['id']
                    recommendations.append({'room_id': recommended_room_id, 'similarity': score[1]})

        recommended_rooms = pd.DataFrame(recommendations).drop_duplicates('room_id')
        return recommended_rooms['room_id'].tolist()
