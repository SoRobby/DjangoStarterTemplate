from django.shortcuts import render, redirect

from apps.accounts.models import Account
from libs.utils.utils import send_notification
from .models import Post
from .forms import PostForm

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
    context = {}
    if request.method == 'POST':

        # Check if form is valid
        form = PostForm(request.POST)
        if form.is_valid():
            print('FORM IS VALID')
        else:
            print('FORM IS NOT VALID')


        # Get post data
        save_type = request.POST.get('save_type')
        title = request.POST.get('title')
        content = request.POST.get('content')
        release_status = request.POST.get('release_status')

        allow_comments = request.POST.get('allow_comments') == 'true'
        allow_sharing = request.POST.get('allow_sharing') == 'true'

        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')

        lead_author = request.POST.get('lead_author')

        # Get lead author by email
        lead_author = Account.objects.get(email=lead_author)

        # Print all the POST out
        print(request.POST)

        # Create blog post
        mew_post = Post.objects.create(title=title,
                                       content=content,
                                       release_status=release_status,
                                       created_by=request.user,
                                       modified_by=request.user,
                                       lead_author=lead_author,
                                       meta_title=meta_title,
                                       meta_description=meta_description,
                                       meta_keywords=meta_keywords,
                                       allow_comments=allow_comments,
                                       allow_sharing=allow_sharing)

        mew_post.authors.add(request.user)

        # Redirect user to edit_post
        send_notification(request, tag='success', title='Blog post created',
                          message='Your post has been successfully created')
        return redirect('blog:edit-post', uuid=mew_post.uuid)

    context['release_status_choices_as_list'] = Post.get_release_status_choices_as_list()
    return render(request, 'blog/create-post.html', context)


def edit_post(request, uuid):
    post = Post.objects.get(uuid=uuid)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post.title = title
        post.content = content
        post.save()
        send_notification(request, tag='success', title='Blog post saved',
                          message='Your post has been successfully saved')

    return render(request, 'blog/edit-post.html', {'post': post})


def delete_post(request, uuid):
    print('DELETING BLOG POST.')
    post = Post.objects.get(uuid=uuid)
    post.delete()
    send_notification(request, tag='success', title='Blog post deleted',
                      message='Your post has been successfully deleted')

    return redirect('blog:post-list')
