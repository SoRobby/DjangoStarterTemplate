import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, 'blog/content/')
    base_url = urljoin(settings.MEDIA_URL, 'blog/content/')

# class CustomStorage(FileSystemStorage):
#     print('Storage called...')
#
#     def save(self, instance):
#         print('Save called...')
#
#         # Print all attributes of the content object
#         print(dir(Post.uuid))
#
#         # # Get the post instance associated with this file
#         # post = Post.objects.get(id=content.instance.id)
#         #
#         # # Generate a new file path based on the post's UUID
#         # new_name = os.path.join(f'blog/images/{post.uuid}/', name)
#         #
#         # # Call the parent class's save method with the new file path
#         # return super().save(new_name, content, max_length)
#
#     location = os.path.join(settings.MEDIA_ROOT, 'blog/images/')
#     base_url = urljoin(settings.MEDIA_URL, 'blog/images/')
