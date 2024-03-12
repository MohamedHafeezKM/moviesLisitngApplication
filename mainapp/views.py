from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers

from mainapp.serializers import UserSerializer,MovieSerializer,FavoriteSerializer,ReviewSerializer
from mainapp.models import Movie,Favorite,Review

class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        
        else:
            return Response(data=serializer.errors)
        

class MovieView(viewsets.ModelViewSet):
    serializer_class=MovieSerializer
    queryset=Movie.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]


    # we are implmenting add to fav fn in MovieView, movie can be listed and added to fav by Customers/Users
    @action(methods=['put'],detail=True)
    def add_to_favorites(self,request,*args,**kwargs):
        movie_id=kwargs.get('pk')
        movie_obj=Movie.objects.get(id=movie_id)
        if movie_obj in request.user.favroites.movie.all():
            return Response(data={'message':'This movie already added before to favorites'})
        else:
            favorite_obj=request.user.favroites
            serializer=FavoriteSerializer(data=request.data,instance=favorite_obj)
            
    
            if serializer.is_valid():
                serializer.instance.movie.add(movie_obj)
                return Response(data=serializer.data)
    
            else:
                return Response(data=serializer.errors)

    @action(methods=['put'],detail=True)
    def remove_from_favorites_moviepage(self,request,*args,**kwargs):
        movie_id=kwargs.get('pk')
        movie_obj=Movie.objects.get(id=movie_id)
        request.user.favroites.movie.remove(movie_obj)
        return Response(data={'message':'This movie has been remove from favorites!'})    
    
    
    @action(methods=['post'],detail=True)
    def add_review(self, request, *args, **kwargs):
        movie_id=kwargs.get('pk')
        movie_obj=Movie.objects.get(id=movie_id)
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie_obj,user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(dat=serializer.errors)

    #blocking these 3 meathods for Users to use
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied!')
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied!')
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied!')
    

class FavoriteView(viewsets.ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        user_fav=request.user.favroites
        deserialization=FavoriteSerializer(user_fav,many=False)
        return Response(data=deserialization.data)
    
    @action(methods=['put'],detail=True)
    def remove_from_favorites(self,request,*args,**kwargs):
        movie_id=kwargs.get('pk')
        movie_obj=Movie.objects.get(id=movie_id)
        favorite_obj=request.user.favroites
        serializer=FavoriteSerializer(data=request.data,instance=favorite_obj)
        

        if serializer.is_valid():
            serializer.instance.movie.remove(movie_obj)
            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)
        

class ReviewView(viewsets.ModelViewSet):
    serializer_class=ReviewSerializer
    queryset=Review.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # def get_queryset(self):
    #     qs=Review.objects.filter(user=self.request.user)
    #     return qs
    
    def perform_update(self, serializer):
        token_user=self.request.user
        review_owner=self.get_object().user
        if token_user==review_owner:
            return super().perform_update(serializer)
        else:
            raise serializers.ValidationError('Owner Permission Required')
        
    def perform_destroy(self, instance):
        token_user=self.request.user
        review_owner=self.get_object().user
        if token_user==review_owner:
            return super().perform_destroy(instance)
        else:
            raise serializers.ValidationError('Owner Permission Required*')

        
        

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied')
    
    def retrieve(self, request, *args, **kwargs):
       
        raise serializers.ValidationError('Permission Denied')
    
    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied')