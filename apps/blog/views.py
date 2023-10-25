import logging
import os
from uuid import uuid4

from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.models import Account
from apps.analytics.views_registry import register_view
from libs.utils.utils import process_image, send_notification, save_file_to_field
from .forms import ArticleForm
from .models import Article, upload_to_featured_images, Comment


# Create your views here.
def article_list(request):
    content = {}

    published_articles = Article.objects.published()
    content['published_articles'] = published_articles

    # Check if user is admin/superuser
    if request.user.is_superuser:
        unpublished_articles = Article.objects.not_published()
        content['unpublished_articles'] = unpublished_articles



    if request.META.get('HTTP_HX_REQUEST'):
        logging.debug('Request is HTMX')
        return render(request, 'blog/partials/articles-list.html', content)
    else:
        logging.debug('Request is not HTMX')
        return render(request, 'blog/articles-list.html', content)




def does_user_have_access(article: Article, user) -> bool:
    """
    Check if a user has access to a given object.

    Parameters:
    - article: The object to check access for. It should have a 'lead_author' attribute.
    - user: The user for whom access is being checked.

    Returns:
    - bool: True if the user has access, False otherwise.
    """
    if user.is_authenticated:
        if article.lead_author == user or user.is_staff or user.is_admin or user.is_superuser:
            return True

    return False


@register_view(namespace="blog", url_name="post", app_name="blog", model=Article)
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'

    # if you need to perform additional operations, you can override the get_context_data method
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # add any additional context if needed
    #     return context


def create_article(request):
    context = {}

    if request.user.is_authenticated:

        if request.method == 'POST':

            # Check if form is valid
            # form = ArticleForm(request.POST)
            # if form.is_valid():
            #     print('FORM IS VALID')
            # else:
            #     print('FORM IS NOT VALID')

            # Get post data
            save_type = request.POST.get('save_type')
            title = request.POST.get('title')

            if len(title) == 0:
                title = f'Untitled {timezone.now().strftime("%Y-%m-%d %H%M%S")}'

            content = request.POST.get('content')
            release_status = request.POST.get('release_status')

            allow_comments = request.POST.get('allow_comments') == 'true'
            allow_sharing = request.POST.get('allow_sharing') == 'true'

            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')

            lead_author = request.POST.get('lead_author_email')

            # Get lead author by email
            lead_author = Account.objects.get(email=lead_author)

            # Print all the POST out
            print(request.POST)

            # Create blog post
            mew_post = Article.objects.create(title=title,
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

            return redirect('blog:edit-article', uuid=mew_post.uuid)

        form = ArticleForm()
        context['form'] = form
        context['release_status_choices_as_list'] = Article.get_release_status_choices_as_list()
        context['get_visibility_choices_as_list'] = Article.get_visibility_choices_as_list()

        return render(request, 'blog/edit/create-article.html', context)

    else:
        return redirect('home')


def edit_article(request, uuid):
    logging.debug('[EDIT_ARTICLE] Called')
    context = {}
    article = Article.objects.get(uuid=uuid)
    user = request.user

    if does_user_have_access(article, user):

        logging.debug(article.FEATURED_IMAGE_ASPECT_RATIO)

        print(Article._meta.get_field('featured_image').name)
        print(upload_to_featured_images(article, 'raw.png'))

        if request.method == 'POST':

            # Get post data
            if 'cropper-distance-x' in request.POST:
                if request.POST.get('cropper-distance-x') != '':
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

                    if image_crop_width / image_crop_height != article.FEATURED_IMAGE_ASPECT_RATIO:
                        logging.debug(f'[EDIT_ARTICLE] Image aspect ratio is not\
                        {str(article.FEATURED_IMAGE_ASPECT_RATIO)}')
                    else:
                        logging.debug(f'[EDIT_ARTICLE] Image aspect ratio is not\
                        {str(article.FEATURED_IMAGE_ASPECT_RATIO)}')

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
                        model_instance=article,
                        field_name='featured_image_raw',
                        file=featured_image_raw_file,
                        directory_path=upload_to_featured_images(article, None),
                        file_name=f'raw.{featured_image_raw.format.lower()}'
                    )
                    # blog_post.featured_image_raw.save(f'raw-{current_datetime}.{featured_image_raw.format.lower()}',\
                    # featured_image_raw_file)

                    # Featured image logic
                    process_image(
                        image=featured_image_raw,
                        crop_dimensions=crop_dimensions,
                        resize_dimensions=article.FEATURED_IMAGE_SIZE,
                        file_format='png'
                    )
                    save_file_to_field(
                        model_instance=article,
                        field_name='featured_image',
                        file=featured_image_raw_file,
                        directory_path=upload_to_featured_images(article, None),
                        file_name=f'featured.webp'
                    )
                    # blog_post.featured_image.save(f'featured-{current_datetime}.webp', featured_image_file)

                    # Featured image thumbnail logic
                    featured_image_thumbnail_file = process_image(
                        image=featured_image_raw,
                        crop_dimensions=crop_dimensions,
                        resize_dimensions=article.FEATURED_IMAGE_THUMBNAIL_SIZE,
                        file_format='png'
                    )
                    save_file_to_field(
                        model_instance=article,
                        field_name='featured_image_thumbnail',
                        file=featured_image_thumbnail_file,
                        directory_path=upload_to_featured_images(article, None),
                        file_name=f'thumbnail.webp'
                    )
                    # blog_post.featured_image_thumbnail.save(f'thumbnail-{current_datetime}.webp',\
                    # featured_image_thumbnail_file)

                    article.save()

                else:
                    logging.debug('[EDIT_POST] Cropper values are empty and no image was uploaded')

            form = ArticleForm(request.POST, instance=article)

            # print(request.POST)

            # form = ArticleForm(request.POST)
            if form.is_valid():
                logging.debug('[EDIT_POST] Form is valid')
                form.save()

                send_notification(request, tag='success', title='Blog post saved',
                                  message='Your article has been successfully saved')
            else:
                logging.debug('[EDIT_POST] Form is not valid')

                error_message = 'An unexpected error occurred while saving your article. Please try again later.'

                # Include form errors in the message
                form_errors = form.errors.as_text()
                if form_errors:
                    error_message += f" Errors: {form_errors}"

                send_notification(request, tag='error', title='Unable to save post',
                                  message=error_message)

        context['form'] = ArticleForm(instance=article)
        context['article'] = article
        return render(request, 'blog/edit/edit-article.html', context)
    else:
        return redirect('home')


@csrf_exempt
def upload_article_image(request, uuid):
    # Supported image formats
    supported_image_formats = ['jpg', 'png', 'gif', 'jpeg', 'git', 'pjeg']

    print('[BLOG.UPLOAD_IMAGE] Called')
    # book = Book.objects.get(id=book_id)

    if request.method != 'POST':
        return JsonResponse({"Error Message": "Wrong request"})

    article = Article.objects.get(uuid=uuid)

    print(f'article = {article}')

    file_obj = request.FILES['file']
    file_name_suffix = file_obj.name.split('.')[-1]

    print('Debug 01')

    if file_name_suffix not in supported_image_formats:
        return JsonResponse(
            {"Error Message": f"Wrong file suffix ({file_name_suffix}), supported are {supported_image_formats}"})
    else:
        print('File image format is valid')

    file_path = os.path.join(settings.MEDIA_ROOT, 'blog', str(article.uuid), 'content', file_obj.name)
    print(f'file_path = {file_path}')

    # Ensure the directory exists. If directory already exists, this function does nothing.
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
        file_obj.name = str(uuid4()) + '.' + file_name_suffix
        file_path = os.path.join(settings.MEDIA_ROOT, 'blog', str(article.uuid), 'content', file_obj.name)

    with open(file_path, 'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    article = Article.objects.get(uuid=uuid)
    context = {}
    form = ArticleForm(instance=article)
    context['article'] = article
    context['form'] = form
    return JsonResponse({
        "Message": "Image upload successfully",
        "location": os.path.join(settings.MEDIA_URL, 'blog', str(article.uuid), 'content', file_obj.name)
    })


def add_comment(request, article_uuid):
    # Get the article by it's uuid
    article = get_object_or_404(Article, uuid=article_uuid)
    print(f'article.slug = {article.slug}')

    if request.method == 'POST':
        # Get the comment content
        if request.user.is_authenticated:
            comment_content = request.POST.get('comment')
            print(comment_content)

            comment = Comment.objects.create(
                article=article,
                user=request.user,
                content=comment_content
            )

    # redirect_url = reverse('article', kwargs={'slug': article.slug})
    # return redirect(redirect_url)
    # return redirect(ArticleDetailView.as_view(), slug=article.slug)
    return redirect(reverse('blog:article', kwargs={'slug': article.slug}))


# def like_comment(request, comment_uuid):

def delete_article(request, uuid):
    """
    Soft deletes an article. Article is not deleted from the database. Article and all artical data is only deleted
    from the database through the admin panel.
    """
    logging.debug(f'[BLOG.DELETE_POST] Soft deleting blog post of uuid={uuid}')

    # Only the blog post owner or superuser can delete a blog post
    post_to_delete = Article.objects.get(uuid=uuid)

    # Get the current user
    user = request.user

    valid_users = [post_to_delete.created_by, post_to_delete.lead_author]

    if user in valid_users or user.is_staff or user.is_superuser:
        post_to_delete.deleted_by = user
        post_to_delete.is_deleted = True
        post_to_delete.save()

    send_notification(request, tag='success', title='Blog post deleted',
                      message='Your post has been successfully deleted')

    return redirect('blog:article-list')
