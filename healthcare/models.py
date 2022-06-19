from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    product_review = models.IntegerField(default=0)
    image = models.CharField(max_length=200)
    
    def __str__(self):
        return self.product_name

class Appuser(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number=models.IntegerField(null=False, unique=True)
    email=models.EmailField(max_length=50, null=True)

    def __str__(self):
        return str(self.user)

        