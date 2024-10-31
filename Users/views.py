from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Person
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
# from .facial_recognition import find_matching_user
from django.conf import settings
import os
import json
import base64

import cv2
import numpy as np
# from .models import User  # Assuming your user model is called User

from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE', '')})

@csrf_exempt
def get_all_persons(request):
    if request.method == 'GET':
        persons = Person.objects.all()
        persons_data = [
            {
                'id': person.id,
                'username': person.username,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'role': person.role,
                'date_of_birth': person.date_of_birth,
                'profile_picture': person.profile_picture.url if person.profile_picture else None,
                'is_active': person.is_active,
                'points': person.points,
            } for person in persons
        ]
        return JsonResponse(persons_data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_person(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_picture = data.get('profile_picture', 'profile_pics/image.png')  # Image par défaut

            person = Person(
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                role=data.get('role', 'student'),
                date_of_birth=data.get('date_of_birth'),
                is_active=data.get('is_active', True),
                points=data.get('points', 0),
                profile_picture=profile_picture  # Assigner l'image de profil par défaut
            )

            password = data.get('password')
            if not password:
                return JsonResponse({'error': 'Le mot de passe est obligatoire.'}, status=400)

            person.set_password(password)
            person.save()

            response_data = {
                'id': person.id,
                'username': person.username,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'role': person.role,
                'date_of_birth': person.date_of_birth,
                'profile_picture': person.profile_picture.url if person.profile_picture else None,
                'is_active': person.is_active,
                'points': person.points,
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_person_detail(request, pk):
    if request.method == 'GET':
        person = get_object_or_404(Person, pk=pk)
        person_data = {
            'id': person.id,
            'username': person.username,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email,
            'role': person.role,
            'date_of_birth': person.date_of_birth,
            'profile_picture': person.profile_picture.url if person.profile_picture else None,
            'is_active': person.is_active,
            'points': person.points,
        }
        return JsonResponse(person_data)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_person(request, pk):
    if request.method == 'PUT':
        person = get_object_or_404(Person, pk=pk)
        try:
            data = json.loads(request.body)
            person.username = data.get('username', person.username)
            person.first_name = data.get('first_name', person.first_name)
            person.last_name = data.get('last_name', person.last_name)
            person.email = data.get('email', person.email)
            person.role = data.get('role', person.role)
            person.date_of_birth = data.get('date_of_birth', person.date_of_birth)
            person.is_active = data.get('is_active', person.is_active)
            person.points = data.get('points', person.points)
            person.save()
            person_data = {
                'id': person.id,
                'username': person.username,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'role': person.role,
                'date_of_birth': person.date_of_birth,
                'profile_picture': person.profile_picture.url if person.profile_picture else None,
                'is_active': person.is_active,
                'points': person.points,
            }
            return JsonResponse(person_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_person(request, pk):
    if request.method == 'DELETE':
        person = get_object_or_404(Person, pk=pk)
        person.delete()
        return JsonResponse({'message': 'Person deleted successfully'}, status=204)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Generate a single access token with custom claims
                access_token = AccessToken.for_user(user)
                access_token['role'] = user.role  # Adding role as a custom claim

                return JsonResponse({
                    'token': str(access_token),
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def toggle_active_status(request, pk):
    if request.method == 'PUT':
        try:
            person = get_object_or_404(Person, pk=pk)

            # Toggle the is_active status
            person.is_active = not person.is_active
            person.save()  # Save the updated status to the database

            # Return a success response with all the user attributes
            return JsonResponse({
                'id': person.id,
                'username': person.username,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'role': person.role,
                'date_of_birth': person.date_of_birth,
                'profile_picture': person.profile_picture.url if person.profile_picture else None,
                'is_active': person.is_active,
                'points': person.points,
                'message': "L'état de l'utilisateur a été mis à jour avec succès."
            }, status=200)
        
        except Exception as e:
            # Return an error response in case of any issues
            return JsonResponse({'error': str(e)}, status=400)
    
    # Return an error response if the request method is not PUT
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def update_profile_picture(request, pk):
    if request.method == 'POST':  # Use POST for file uploads
        person = get_object_or_404(Person, pk=pk)
        try:
            # Check if a profile picture was uploaded
            if 'profile_picture' in request.FILES:
                # Remove old profile picture if it exists
                if person.profile_picture:
                    old_picture_path = os.path.join(settings.MEDIA_ROOT, person.profile_picture.name)
                    if os.path.isfile(old_picture_path):
                        os.remove(old_picture_path)

                # Update with new profile picture
                person.profile_picture = request.FILES['profile_picture']
                person.save()

                # Return success response with updated profile picture URL
                return JsonResponse({
                    'id': person.id,
                    'profile_picture': person.profile_picture.url if person.profile_picture else None,
                    'message': 'Profile picture updated successfully'
                }, status=200)
            else:
                return JsonResponse({'error': 'No profile picture provided'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_password(request, pk):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not old_password or not new_password:
                return JsonResponse({'error': 'Both old and new passwords are required.'}, status=400)

            person = get_object_or_404(Person, pk=pk)

            # Verify old password
            if not check_password(old_password, person.password):
                return JsonResponse({'error': 'Old password is incorrect.'}, status=400)

            # Set new password
            person.set_password(new_password)
            person.save()

            # Update session so the user stays logged in
            update_session_auth_hash(request, person)

            return JsonResponse({'message': 'Password updated successfully.'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def create_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_picture = data.get('profile_picture', 'profile_pics/image.png')  # Image par défaut

            person = Person(
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                role=data.get('role', 'admin'),
                date_of_birth=data.get('date_of_birth'),
                is_active=data.get('is_active', True),
                points=data.get('points', 0),
                profile_picture=profile_picture  # Assigner l'image de profil par défaut
            )

            password = data.get('password')
            if not password:
                return JsonResponse({'error': 'Le mot de passe est obligatoire.'}, status=400)

            person.set_password(password)
            person.save()

            response_data = {
                'id': person.id,
                'username': person.username,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'role': person.role,
                'date_of_birth': person.date_of_birth,
                'profile_picture': person.profile_picture.url if person.profile_picture else None,
                'is_active': person.is_active,
                'points': person.points,
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
 





###############

@csrf_exempt
def load_and_preprocess_image(image_path):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}.")
        return None
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use OpenCV's face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    
    # Ensure only one face is detected
    if len(faces) != 1:
        print(f"Error: Expected one face in {image_path}, but found {len(faces)}.")
        return None
    
    # Crop the detected face
    (x, y, w, h) = faces[0]
    face_region = gray_image[y:y+h, x:x+w]
    return face_region

@csrf_exempt
def find_matching_user(uploaded_image_path):
    uploaded_face = load_and_preprocess_image(uploaded_image_path)
    if uploaded_face is None:
        print("No face detected in the uploaded image.")
        return None

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Iterate through each image in media/profile_pics
    profile_pics_dir = os.path.join(settings.MEDIA_ROOT, "profile_pics")
    for file_name in os.listdir(profile_pics_dir):
        user_image_path = os.path.join(profile_pics_dir, file_name)
        
        # Skip non-image files
        if not user_image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        
        # Load and preprocess the user's profile picture
        user_face = load_and_preprocess_image(user_image_path)
        if user_face is None:
            print(f"No face detected in {file_name}. Skipping.")
            continue
        
        # Train the recognizer on the user face and predict against the uploaded face
        recognizer.train([user_face], np.array([1]))
        label, confidence = recognizer.predict(uploaded_face)
        
        # Debug: Print confidence level for each comparison
        print(f"Comparing with {file_name}: confidence={confidence}")
        
        # A confidence threshold for matching (confidence of 0.0 should indicate a perfect match)
        if confidence == 0.0 or confidence < 50:  # Adjust threshold if necessary
            # Attempt to find the corresponding user by matching the profile picture filename
            user = Person.objects.filter(profile_picture=f"profile_pics/{file_name}").first()
            if user:
                print(f"Match found for user: {user.username} with confidence={confidence}")
                return user  # Return the matched user
    
    return None

import logging
logger = logging.getLogger(__name__)


@csrf_exempt  # Exempts CSRF requirements for this view
def authenticate_with_face(request):
    logger.info("Request received for facial authentication.")
    
    if request.method == 'POST' and request.FILES.get('photo'):
        try:
            # Process the uploaded image
            photo = request.FILES['photo']
            temp_image_path = 'temp_uploaded_image.jpg'
            with open(temp_image_path, 'wb+') as temp_image:
                for chunk in photo.chunks():
                    temp_image.write(chunk)

            # Attempt to find a matching user
            match = find_matching_user(temp_image_path)
            os.remove(temp_image_path)

            if match:
                # Generate a single access token with the user role claim
                access_token = AccessToken.for_user(match)
                access_token['role'] = match.role  # Add custom claim for the user role

                logger.info(f"Authentication successful for user: {match.username}")

                return JsonResponse({
                    'success': True,
                    'token': str(access_token),  # Return access token to frontend
                    'username': match.username,
                }, status=200)

            logger.warning("No matching user found.")
            return JsonResponse({'success': False, 'message': 'No match found.'}, status=401)

        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    logger.error("Invalid request: No photo or incorrect method.")
    return JsonResponse({'error': 'Invalid request'}, status=400)