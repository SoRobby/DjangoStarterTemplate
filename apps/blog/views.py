from django.shortcuts import render

from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.published()
    return render(request, 'blog/post-list.html', {'posts': posts})


def post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post.html', {'post': post})


def create_post(request):
    return render(request, 'blog/create-post.html')
