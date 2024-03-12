from django.contrib import admin

# Register your models here.

from mainapp.models import Movie,Casting

admin.site.register(Movie)
admin.site.register(Casting)