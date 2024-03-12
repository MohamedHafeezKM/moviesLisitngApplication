from rest_framework import serializers

from django.contrib.auth.models import User

from mainapp.models import Movie,Review,Favorite,Casting


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','email']
        read_only_fields=['id']

    def create(self, validated_data):  #for encryption
        return User.objects.create_user(**validated_data)
    
class CastingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Casting
        fields=['name','created_at','updated_at','is_active']

class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'
        read_only_fields=['id','user','movie','created_at','updated_at','is_active']


class MovieSerializer(serializers.ModelSerializer):
    casting=CastingSerializer(read_only=True,many=True)
    movie_reviews=ReviewSerializer(read_only=True,many=True)
    class Meta:
        model=Movie
        fields='__all__'
        read_only_fields=['name','image','casting','created_at','updated_at','is_active','year','detail','movie_reviews']


class FavoriteSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    movie=MovieSerializer(read_only=True,many=True)
    favorite_movie_count=serializers.CharField(read_only=True)
    class Meta:
        model=Favorite
        fields='__all__'

        read_only_fields=['id','user','movie','created_at','updated_at','is_active','favorite_movie_count']
        

