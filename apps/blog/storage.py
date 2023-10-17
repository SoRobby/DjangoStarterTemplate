import logging
import os
from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):
    logging.debug('[CUSTOM_STORAGE] Called')
    current_date = datetime.now().strftime('%Y-%m-%d')
    location = os.path.join(settings.MEDIA_ROOT, f'blog/content/{current_date}/')
    base_url = urljoin(settings.MEDIA_URL, f'blog/content/{current_date}/')



