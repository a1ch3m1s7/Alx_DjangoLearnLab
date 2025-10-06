# Create your views here.
from django.shortcuts import render
from .models import Post
from datetime import datetime

def home(request):
    posts = Post.objects.all().order_by('-published_date')  # newest first
    context = {
        'posts': posts,
        'year': datetime.now().year,  # for footer
    }
    return render(request, 'blog/home.html', context)
