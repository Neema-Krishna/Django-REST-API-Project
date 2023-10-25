from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

# class Movie(models.Model):
#     name=models.CharField(max_length=50)
#     description=models.CharField(max_length=200)
#     active=models.BooleanField(default=True)
    
    
#     def __str__(self):
#         return self.name

class StreamPlatform(models.Model):
    name=models.CharField(max_length=50)
    about=models.CharField(max_length=50)
    website=models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Watchlist(models.Model):
    title=models.CharField(max_length=50)
    storyline=models.CharField(max_length=200)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchlist1')
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    avg_rating=models.FloatField(default=0)
    avg_numbering=models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.title

class Review(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    description=models.CharField(max_length=50)
    watchlist=models.ForeignKey(Watchlist,on_delete=models.CASCADE,related_name='reviews')
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Rating-" + str(self.rating) +'  | ' + 'Title-' + self.watchlist.title
    
    
    
    
