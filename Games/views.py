from django.shortcuts import render

import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz, Question


@csrf_exempt
def quiz_list(request):
    if request.method == 'GET':
        categories = list(Quiz.objects.values('id', 'name', 'subject'))
        return JsonResponse(categories, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz = Quiz.objects.create(
                name=data.get('name'),
                subject=data.get('subject')
            )
            return JsonResponse({'id': quiz.id, 'name': quiz.name, 'subject': quiz.subject})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def singlequiz(request,Quizid):
    try:
        quiz = Quiz.objects.get(id=Quizid)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': quiz.id, 'name': quiz.name, 'subject': quiz.subject})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            quiz.name = data.get('name', quiz.name)
            quiz.subject = data.get('subject', quiz.subject)
            quiz.save()
            return JsonResponse({'id': quiz.id, 'name': quiz.name, 'subject': quiz.subject})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)


    elif request.method == 'DELETE':
        quiz.delete()
        return JsonResponse({'message': 'Quiz deleted successfully'})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

