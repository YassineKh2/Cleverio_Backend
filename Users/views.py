from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Person
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


import json

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
            # Créer l'objet Person
            person = Person(
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                role=data.get('role', 'student'),
                date_of_birth=data.get('date_of_birth'),
                is_active=data.get('is_active', True),
                points=data.get('points', 0),
            )
            # Définir le mot de passe de manière sécurisée
            password = data.get('password')
            if not password:
                return JsonResponse({'error': 'Le mot de passe est obligatoire.'}, status=400)
            
            person.set_password(password)  # Utiliser set_password pour hacher le mot de passe
            person.save()

            # Préparer les données de la réponse
            response_data = {
                'id': person.id,
                'username': person.username,
                'first_name': person.first_name,
                'last_name': person.last_name,
                'email': person.email,
                'role': person.role,
                'date_of_birth': person.date_of_birth,
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
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                # Add custom claims, e.g., role
                refresh['role'] = user.role  # Assuming `role` is a field on the user model

                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)