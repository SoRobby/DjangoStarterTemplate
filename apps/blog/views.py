import logging

from PIL import Image
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from apps.accounts.models import Account
from apps.analytics.mixins import ObjectViewMixin
from libs.utils.utils import process_image, send_notification, save_file_to_field
from .forms import PostForm
from .models import Post, upload_to_featured_images


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


# def post(request, slug):
#     context = {}
#     single_post = Post.objects.get(slug=slug)
#     context['post'] = single_post
#     return render(request, 'blog/post.html', context)

class PostDetailView(ObjectViewMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    # if you need to perform additional operations, you can override the get_context_data method
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # add any additional context if needed
    #     return context


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
    blog_post = Post.objects.get(uuid=uuid)

    print('path: ')
    print(Post._meta.get_field('featured_image').name)
    print(upload_to_featured_images(blog_post, 'raw.png'))

    if request.method == 'POST':

        # Get post data
        if 'cropper-distance-x' in request.POST:
            if request.POST.get('cropper-distance-x') != '':
                # current_datetime = get_yyyymmddhhmmss()

                image_crop_x = float(request.POST.get('cropper-distance-x'))
                image_crop_y = float(request.POST.get('cropper-distance-y'))
                image_crop_width = float(request.POST.get('cropper-width'))
                image_crop_height = float(request.POST.get('cropper-height'))

                crop_dimensions = (image_crop_x, image_crop_y, image_crop_width, image_crop_height)

                logging.debug('[EDIT_POST] Cropper values are not empty')
                logging.debug(f'[EDIT_POST] image_crop_x = {image_crop_x}')
                logging.debug(f'[EDIT_POST] image_crop_y = {image_crop_y}')
                logging.debug(f'[EDIT_POST] image_crop_width = {image_crop_width}')
                logging.debug(f'[EDIT_POST] image_crop_height = {image_crop_height}')
                if image_crop_width / image_crop_height != 16 / 9:
                    logging.debug('[EDIT_POST] Image aspect ratio is not 16:9')
                else:
                    logging.debug('[EDIT_POST] Image aspect ratio is 16:9')

                # Get image file that was uploaded
                featured_image_raw = Image.open(request.FILES.get('featured_image'))

                # Featured image logic
                featured_image_raw_file = process_image(
                    image=featured_image_raw,
                    crop_dimensions=None,
                    resize_dimensions=None,
                    file_format=None,
                )
                save_file_to_field(
                    model_instance=blog_post,
                    field_name='featured_image_raw',
                    file=featured_image_raw_file,
                    directory_path=upload_to_featured_images(blog_post, None),
                    file_name=f'raw.{featured_image_raw.format.lower()}'
                )
                # blog_post.featured_image_raw.save(f'raw-{current_datetime}.{featured_image_raw.format.lower()}', featured_image_raw_file)

                # Featured image logic
                featured_image_file = process_image(
                    image=featured_image_raw,
                    crop_dimensions=crop_dimensions,
                    resize_dimensions=(730, 428),
                    file_format='png'
                )
                save_file_to_field(
                    model_instance=blog_post,
                    field_name='featured_image',
                    file=featured_image_raw_file,
                    directory_path=upload_to_featured_images(blog_post, None),
                    file_name=f'featured.webp'
                )
                # blog_post.featured_image.save(f'featured-{current_datetime}.webp', featured_image_file)

                # Featured image thumbnail logic
                featured_image_thumbnail_file = process_image(
                    image=featured_image_raw,
                    crop_dimensions=crop_dimensions,
                    resize_dimensions=(200, 200),
                    file_format='png'
                )
                save_file_to_field(
                    model_instance=blog_post,
                    field_name='featured_image_thumbnail',
                    file=featured_image_thumbnail_file,
                    directory_path=upload_to_featured_images(blog_post, None),
                    file_name=f'thumbnail.webp'
                )
                # blog_post.featured_image_thumbnail.save(f'thumbnail-{current_datetime}.webp', featured_image_thumbnail_file)

                blog_post.save()

            else:
                logging.debug('[EDIT_POST] Cropper values are empty and no image was uploaded')

        form = PostForm(request.POST, instance=blog_post)

        # form = PostForm(request.POST)
        if form.is_valid():
            logging.debug('[EDIT_POST] Form is valid')

            form.save()

            send_notification(request, tag='success', title='Blog post saved',
                              message='Your post has been successfully saved')
        else:
            logging.debug('[EDIT_POST] Form is not valid')

            error_message = 'An unexpected error occurred while saving your post. Please try again later.'

            # Include form errors in the message
            form_errors = form.errors.as_text()
            if form_errors:
                error_message += f" Errors: {form_errors}"

            send_notification(request, tag='error', title='Unable to save post',
                              message=error_message)

    context['form'] = PostForm(instance=blog_post)
    context['post'] = blog_post
    return render(request, 'blog/edit-post.html', context)


def delete_post(request, uuid):
    logging.debug(f'[BLOG.DELETE_POST] Soft deleting blog post of uuid={uuid}')

    # Only the blog post owner or superuser can delete a blog post
    post_to_delete = Post.objects.get(uuid=uuid)

    if post_to_delete.created_by == request.user or post_to_delete.lead_author == request.user or request.user.is_superuser:
        post_to_delete.deleted_by = request.user
        post_to_delete.is_deleted = True
        post_to_delete.save()

    send_notification(request, tag='success', title='Blog post deleted',
                      message='Your post has been successfully deleted')

    return redirect('blog:post-list')
