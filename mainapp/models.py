from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Casting(models.Model):
    name=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def  __str__(self):
        return self.name
    

class Movie(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images',default='none.jpg')
    casting=models.ManyToManyField(Casting,related_name='cast')
    year=models.PositiveIntegerField()
    detail=models.CharField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def  __str__(self):
        return self.name
    
    @property
    def movie_reviews(self):
       return self.filim.all()

class Favorite(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='favroites')
    movie=models.ManyToManyField(Movie,related_name='favorite_movies')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    @property
    def favorite_movie_count(self):
        return self.movie.all().count()




def create_favorites(sender,instance,created,**kwargs):
    if created:
        Favorite.objects.create(user=instance)

post_save.connect(create_favorites,sender=User)

class Review(models.Model):
   
    comment=models.CharField(max_length=400)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='filim')
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='person')
    options=(
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    )
    rating=models.CharField(max_length=200,choices=options)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    

    def __str__(self):
        return self.rating
