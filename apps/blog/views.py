from django.shortcuts import render, redirect

from apps.accounts.models import Account
from libs.utils.utils import send_notification
from .forms import PostForm
from .models import Post
from django.utils import timezone
import zoneinfo
import datetime

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
    single_post = Post.objects.get(slug=slug)
    return render(request, 'blog/post.html', {'post': single_post})


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
    context = {}
    single_post = Post.objects.get(uuid=uuid)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        # form = PostForm(request.POST)
        if form.is_valid():
            print('FORM IS VALID')
            print(form.cleaned_data)
            form.save()

            send_notification(request, tag='success', title='Blog post saved',
                              message='Your post has been successfully saved')
        else:
            error_message = 'An unexpected error occurred while saving your post. Please try again later.'

            # Include form errors in the message
            form_errors = form.errors.as_text()
            if form_errors:
                error_message += f" Errors: {form_errors}"

            send_notification(request, tag='error', title='Unable to save post',
                              message=error_message)
            # send_notification(request, tag='error', title='Unable to save post',
            #                   message='An unexpected error occurred while saving your post. Please try again later.')

    context['post'] = single_post
    return render(request, 'blog/edit-post.html', context)


def delete_post(request, uuid):
    print('DELETING BLOG POST.')
    post = Post.objects.get(uuid=uuid)
    post.delete()
    send_notification(request, tag='success', title='Blog post deleted',
                      message='Your post has been successfully deleted')

    return redirect('blog:post-list')
