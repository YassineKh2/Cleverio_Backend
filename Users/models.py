from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator

# Custom validator for username (alphanumeric only)
username_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message="Le nom d'utilisateur ne peut contenir que des lettres, des chiffres et les caractères @/./+/-/_",
)

class Person(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('student', 'Étudiant'),
    )
    
    # Custom field for user roles
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='student',
        verbose_name='Rôle'
    )
    
    # Custom email field with validation and uniqueness
    email = models.EmailField(
        unique=True, 
        validators=[EmailValidator(message="Veuillez entrer une adresse e-mail valide.")],
        verbose_name='Adresse e-mail'
    )
    
    # Custom validator for username
    username = models.CharField(
        max_length=150, 
        unique=True,
        validators=[username_validator],
        verbose_name='Nom d\'utilisateur'
    )
    
    # Optional date of birth field
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Date de naissance'
    )
    
    # Profile picture field without extra validation
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True, 
        verbose_name='Photo de profil'
    )
    
    # Boolean field to determine if the user is active
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Actif'
    )
    
    # Points field to track user points
    points = models.IntegerField(
        default=0,
        verbose_name='Points'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "Person"
