from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# class CustomUserManager(BaseUserManager):
#     def create_User(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("This field must not be Null")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username 