from django.db import models


class Question(models.Model):
    name = models.CharField(max_length=30)
    points = models.PositiveIntegerField()
    option1 = models.CharField(max_length=30)
    option2 = models.CharField(max_length=30)
    option3 = models.CharField(max_length=30)
    option4 = models.CharField(max_length=30)
    answer = models.CharField(max_length=30)
    Quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)

    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
