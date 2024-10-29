from django.db import models

# Create your models here.

class Room(models.Model):

    status_list = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('In_progress', 'In_progress'),
    ]

    name = models.CharField(max_length=40)
    subject = models.CharField(max_length=40)
    description= models.TextField()
    image= models.ImageField(null=True, upload_to="rooms/")
    status=models.CharField(max_length=20, choices=status_list)


    max_participants = models.IntegerField(default=10)
    is_private = models.CharField(max_length=40)

    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):

        return self.name