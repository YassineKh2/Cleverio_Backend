from django.contrib import admin
from .models import Category, Game,Purchase

admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Purchase)