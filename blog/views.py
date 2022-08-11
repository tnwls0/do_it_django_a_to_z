from django.shortcuts import render
from django.views.generic import ListView, DetailView
from. models import Post

class PostList(ListView): #상속받아서 사용
    model = Post
    ordering = '-pk'

# *신규
class PostDetail(DetailView):
    model = Post



# Create your views here.