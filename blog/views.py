from django.shortcuts import render
from django.views.generic import ListView
from. models import Post

class PostList(ListView): #상속받아서 사용
    model = Post
    ordering = '-pk'

# Create your views here.