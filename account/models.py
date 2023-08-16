from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from django.utils import timezone

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('prefer_not_to_say', 'Prefer not to say'),
)

ACCOUNT_TYPE_CHOICES = (
    ('savings', 'Savings Account'),
    ('current', 'Current Account'),
    
)  

class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, full_name, contact_number, password=None , **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, full_name=full_name, contact_number=contact_number ,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, contact_number, password=None , **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, full_name ,contact_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]+$',
        message='Username must contain only letters, digits, and underscores.',
        code='invalid_username'
    )
 

 
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator],
        help_text='Required. 30 characters or fewer. Letters, digits, and underscores only.',
        error_messages={
            'unique': 'A user with that username already exists.',
        }
    )


  


 

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=15 , default='none')
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES ,default='none')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES , default='none')
    account_number = models.CharField(max_length=4, unique=True, blank=True, null=True)
    ifsc = models.CharField(max_length=5, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pin = models.CharField(max_length=4, blank=True)

 
      
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','username' , 'contact_number']

    objects = CustomUserManager()  

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.date_joined = timezone.now()
        super().save(*args, **kwargs)
    
   

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email


    


