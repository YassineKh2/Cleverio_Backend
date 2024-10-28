from django import forms
from .models import Category, Game

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'points', 'picture', 'category', 'description', 'stock_quantity']
