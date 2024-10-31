import re

from django.shortcuts import render

import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel, Field

from .models import Quiz, Question
import os
from groq import Groq
import instructor

api_key = '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'


class QuestionClass(BaseModel):
    question: str
    options: list[str] = Field(..., min_items=4, max_items=4)
    answer: str


@csrf_exempt
def quiz_list(request):
    if request.method == 'GET':
        quizzes = Quiz.objects.prefetch_related('question_set').values('id', 'name', 'subject')
        categories = []
        for quiz in quizzes:
            questions = list(Question.objects.filter(Quiz_id=quiz['id']).values(
                'id', 'name', 'points', 'option1', 'option2', 'option3', 'option4', 'answer'
            ))
            quiz['questions'] = questions
            categories.append(quiz)

        return JsonResponse(categories, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz = Quiz.objects.create(
                name=data.get('name'),
                subject=data.get('subject')
            )

            client = Groq(api_key=api_key)

            client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        'role': 'system',
                        'content': 'I will provide you with a quiz name and subject. You will need to provide me with 1 Question and the 4 options and the correct answer .'
                                   'i want you to reply ONLY REPLY WITH THIS STRUCTURE "question, option1, option2, option3, option4, answer" for each question.'
                    },
                    {
                        'role': 'user',
                        'content': 'Create a quiz with the name = ' + quiz.name + ' and the subject of' + quiz.subject
                    },
                ],
                model='llama-3.1-70b-versatile',
                response_model=QuestionClass
            )
            response = chat_completion.model_dump_json(indent=2)
            response_dict = json.loads(response)

            name = response_dict.get('question')
            option1 = response_dict.get('options')[0]
            option2 = response_dict.get('options')[1]
            option3 = response_dict.get('options')[2]
            option4 = response_dict.get('options')[3]
            answer = response_dict.get('answer')

            question = Question.objects.create(
                name=name,
                points=20,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                answer=answer,
                Quiz=quiz
            )

            return JsonResponse({'id': quiz.id, 'name': quiz.name, 'subject': quiz.subject})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def singlequiz(request, Quizid):
    try:
        quiz = Quiz.objects.get(id=Quizid)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    if request.method == 'GET':

        questions = list(Question.objects.filter(Quiz_id=quiz.id).values(
            'id', 'name', 'points', 'option1', 'option2', 'option3', 'option4', 'answer'
        ))
        return JsonResponse({
            'id': quiz.id,
            'name': quiz.name,
            'subject': quiz.subject,
            'questions': questions
        })

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


def question_list(request):
    if request.method == 'GET':
        questions = list(
            Question.objects.values('id', 'name', 'points', 'option1', 'option2', 'option3', 'option4', 'answer',
                                    'Quiz'))
        return JsonResponse(questions, safe=False)

    return HttpResponseNotAllowed(['GET', 'POST'])
