from django.shortcuts import render, redirect

from apps.accounts.models import Account
from libs.utils.utils import send_notification
from .models import Post


# Create your views here.
def post_list(request):
    content = {}

    published_posts = Post.objects.published()
    content['published_posts'] = published_posts

    # Check if user is admin/superuser
    if request.user.is_superuser:
        not_published_posts = Post.objects.not_published()
        content['not_published_posts'] = not_published_posts

    return render(request, 'blog/post-list.html', content)


def post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post.html', {'post': post})


def create_post(request):
    if request.method == 'POST':
        # Get blog post title
        title = request.POST.get('title')
        content = request.POST.get('editor')
        allow_comments = request.POST.get('allow_comments')
        allow_sharing = request.POST.get('allow_sharing')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        lead_author = request.POST.get('lead_author')

        # Get lead author by email
        lead_author = Account.objects.get(email=lead_author)

        # Print all the POST out
        print(request.POST)

        # Create blog post
        mew_post = Post.objects.create(title=title, content=content, release_status=Post.RELEASE_STATUS.DRAFT,
                                       created_by=request.user, modified_by=request.user, lead_author=lead_author)
        mew_post.authors.add(request.user)

        # Redirect user to edit_post
        send_notification(request, tag='success', title='Blog post created',
                          message='Your post has been successfully created')
        return redirect('blog:edit-post', uuid=mew_post.uuid)

    return render(request, 'blog/create-post.html')


def edit_post(request, uuid):
    post = Post.objects.get(uuid=uuid)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('editor')
        post.title = title
        post.content = content
        post.save()
        send_notification(request, tag='success', title='Blog post saved',
                          message='Your post has been successfully saved')

    return render(request, 'blog/edit-post.html', {'post': post})
