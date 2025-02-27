from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
 
    def __str__(self):
        return self.username
    
