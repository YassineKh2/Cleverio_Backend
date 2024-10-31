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


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Category, Game

@csrf_exempt
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.select_related('category').values(
            'id', 
            'name', 
            'points', 
            'category__name',
            'description', 
            'stock_quantity',
            'picture'
        )
        games_with_category_name = [
            {
                'id': game['id'],
                'name': game['name'],
                'points': game['points'],
                'category_name': game['category__name'],
                'description': game['description'],
                'stock_quantity': game['stock_quantity'],
                'picture_url': game['picture'] if game['picture'] else None
            }
            for game in games
        ]
        return JsonResponse(games_with_category_name, safe=False)
    
    elif request.method == 'POST':
        try:
            # Access form data and file data separately
            data = request.POST
            category_name = data.get('category_name')
            category, created = Category.objects.get_or_create(name=category_name)

            game = Game.objects.create(
                name=data.get('name'),
                points=data.get('points'),
                picture=request.FILES.get('picture'),  # Handle picture file
                category=category,
                description=data.get('description'),
                stock_quantity=data.get('stock_quantity', 0)
            )
            return JsonResponse({
                'id': game.id,
                'name': game.name,
                'points': game.points,
                'category_name': game.category.name,
                'description': game.description,
                'stock_quantity': game.stock_quantity,
                'picture_url': game.picture.url if game.picture else None
            })
        except (KeyError, Category.DoesNotExist):
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
            'category_name': game.category.name,
            'description': game.description,
            'stock_quantity': game.stock_quantity,
            'picture_url': game.picture.url if game.picture else None  # Add picture URL if it exists
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            game.name = data.get('name', game.name)
            game.points = data.get('points', game.points)
            game.description = data.get('description', game.description)
            game.stock_quantity = data.get('stock_quantity', game.stock_quantity)

            category_name = data.get('category_name')
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)
                game.category = category

            game.save()
            return JsonResponse({
                'id': game.id,
                'name': game.name,
                'points': game.points,
                'category_name': game.category.name,
                'description': game.description,
                'stock_quantity': game.stock_quantity,
                'picture_url': game.picture.url if game.picture else None
            })
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    
    elif request.method == 'DELETE':
        game.delete()
        return JsonResponse({'message': 'Game deleted successfully'})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
