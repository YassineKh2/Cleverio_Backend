import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Game

@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        categories = list(Category.objects.values('id', 'name', 'description'))
        return JsonResponse(categories, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = Category.objects.create(
                name=data.get('name'),
                description=data.get('description')
            )
            return JsonResponse({'id': category.id, 'name': category.name, 'description': category.description})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    
    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': category.id, 'name': category.name, 'description': category.description})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            category.name = data.get('name', category.name)
            category.description = data.get('description', category.description)
            category.save()
            return JsonResponse({'id': category.id, 'name': category.name, 'description': category.description})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({'message': 'Category deleted successfully'})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

@csrf_exempt
def game_list(request):
    if request.method == 'GET':
        games = list(Game.objects.values('id', 'name', 'points', 'category_id', 'description', 'stock_quantity'))
        return JsonResponse(games, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = Category.objects.get(id=data.get('category_id'))
            game = Game.objects.create(
                name=data.get('name'),
                points=data.get('points'),
                picture=data.get('picture'),  # Handle file uploads differently
                category=category,
                description=data.get('description'),
                stock_quantity=data.get('stock_quantity', 0)
            )
            return JsonResponse({
                'id': game.id,
                'name': game.name,
                'points': game.points,
                'category_id': game.category.id,
                'description': game.description,
                'stock_quantity': game.stock_quantity
            })
        except (json.JSONDecodeError, KeyError, Category.DoesNotExist):
            return JsonResponse({'error': 'Invalid data or category not found'}, status=400)
    
    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def game_detail(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': game.id,
            'name': game.name,
            'points': game.points,
            'category_id': game.category.id,
            'description': game.description,
            'stock_quantity': game.stock_quantity
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            game.name = data.get('name', game.name)
            game.points = data.get('points', game.points)
            game.description = data.get('description', game.description)
            game.stock_quantity = data.get('stock_quantity', game.stock_quantity)
            game.save()
            return JsonResponse({
                'id': game.id,
                'name': game.name,
                'points': game.points,
                'category_id': game.category.id,
                'description': game.description,
                'stock_quantity': game.stock_quantity
            })
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    
    elif request.method == 'DELETE':
        game.delete()
        return JsonResponse({'message': 'Game deleted successfully'})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
