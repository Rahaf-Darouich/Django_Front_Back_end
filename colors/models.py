from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid 

# Create your models here.
class User(AbstractUser):
    id = models.CharField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False, 
         max_length=180) 
    red = models.IntegerField(default=10)
    yellow = models.IntegerField(default=10)
    blue = models.IntegerField(default=10)
    green = models.IntegerField(default=10)
   
    # ...
    class Meta:
        app_label = 'colors'

class OrderHistory(models.Model):
    class Status(models.TextChoices):
        ORDER_CONFIRMED = 'ORDER_CONFIRMED', 'ORDER_CONFIRMED'
        COMPLETED = 'Completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,  # Adjust the max_length based on your needs
        choices=Status.choices,
        default=None,  # Default value can be set to None
        null=True,     # Allow null values
        blank=True,    # Allow empty values
    )
    red = models.IntegerField(default=None, null=True)
    yellow = models.IntegerField(default=None, null=True)
    blue = models.IntegerField(default=None, null=True)
    green = models.IntegerField(default=None, null=True)
    is_error = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now)
    user_name = models.CharField(max_length=160)
    error = models.CharField(max_length=120, null=True, default=None)
    



