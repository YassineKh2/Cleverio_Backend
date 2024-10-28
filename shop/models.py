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
