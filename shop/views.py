import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Game ,Purchase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localtime
from django.contrib.auth.models import User

User = get_user_model()

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





@csrf_exempt
def purchase_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            game_id = data.get("game_id")

            # Retrieve the user and game
            user = User.objects.get(id=user_id)
            game = Game.objects.get(id=game_id)

            # Check if the user has enough points
            if user.points < game.points:
                return JsonResponse({'error': 'Not enough points to make this purchase'}, status=400)

            # Check if the game is in stock
            if game.stock_quantity < 1:
                return JsonResponse({'error': 'Game out of stock'}, status=400)

            # Deduct points and update stock quantity
            user.points -= game.points
            game.stock_quantity -= 1
            user.save()
            game.save()

            # Record the purchase
            purchase = Purchase.objects.create(
                user=user,
                game=game,
                points_used=game.points
            )

            return JsonResponse({
                'message': 'Purchase successful',
                'purchase': {
                    'id': purchase.id,
                    'game': game.name,
                    'points_used': game.points,
                    'purchase_date': purchase.purchase_date
                }
            })

        except (User.DoesNotExist, Game.DoesNotExist):
            return JsonResponse({'error': 'User or game not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def user_purchases(request, user_id):
    # Filter purchases by user_id
    try:
        purchases = Purchase.objects.filter(user_id=user_id).select_related('game')
        if not purchases.exists():
            return JsonResponse({"message": "No purchases found for this user."}, status=404)

        # Format the purchase data for the response
        purchases_data = [
            {
                "game": purchase.game.name,
                "points_used": purchase.points_used,
                "purchase_date": localtime(purchase.purchase_date).strftime("%Y-%m-%d %H:%M:%S"),
            }
            for purchase in purchases
        ]
        
        return JsonResponse({"user_id": user_id, "purchases": purchases_data}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({"message": "User or purchases not found."}, status=404)
    

 
def all_users_purchases(request):
    try:
        # Fetch all purchases and prefetch related user and game details
        purchases = Purchase.objects.select_related('user', 'game')

        if not purchases.exists():
            return JsonResponse({"message": "No purchases found."}, status=404)

        # Format the purchase data for the response
        purchases_data = {}
        for purchase in purchases:
            user_id = purchase.user.id
            if user_id not in purchases_data:
                purchases_data[user_id] = {
                    "username": purchase.user.username,
                    "email": purchase.user.email,  # Add email address here
                    "purchases": []
                }
            purchases_data[user_id]["purchases"].append({
                "game": purchase.game.name,
                "points_used": purchase.points_used,
                "purchase_date": localtime(purchase.purchase_date).strftime("%Y-%m-%d %H:%M:%S"),
            })

        return JsonResponse(purchases_data, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_purchase(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        game_name = data.get('game')

        try:
            # Fetch all purchases based on user_id and game_name
            purchases = Purchase.objects.filter(user_id=user_id, game__name=game_name)

            if not purchases.exists():
                return JsonResponse({'error': 'Purchase not found'}, status=404)

            total_refunded = 0
            for purchase in purchases:
                total_refunded += purchase.points_used
                
                # Refund points logic
                user = purchase.user  # Get the user from the purchase instance
                user.points += purchase.points_used  # Refund points
                user.save()

                # Increase the stock quantity of the game
                game = purchase.game  # Get the associated game
                game.stock_quantity += 1  # Increase stock by 1
                game.save()  # Save the updated game

                purchase.delete()  # Delete the purchase

            return JsonResponse({'message': 'Purchases deleted successfully', 'points_refunded': total_refunded}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
