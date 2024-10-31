from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField()  # Points required for purchase
    picture = models.ImageField(upload_to='games/')
    category = models.ForeignKey(Category, related_name='games', on_delete=models.CASCADE)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)
    points_used = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} purchased {self.game.name} on {self.purchase_date.strftime('%Y-%m-%d %H:%M:%S')}"