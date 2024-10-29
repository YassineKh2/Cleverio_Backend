from django.db import models

# Create your models here.
class Art(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='art_images/')  # Requires `Pillow` package
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    art = models.ForeignKey(Art, related_name='comments', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, default='Anonymous')  # Static user field
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user_name} on {self.art.title}'
