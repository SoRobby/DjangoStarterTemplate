# Project's apps sitemaps
from apps.core.sitemaps import CoreStaticSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

# Sitemap URLS
# https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/

# Dictionary of project sitemaps
sitemap_core = {'sitemap': CoreStaticSitemap}

# Sitemap base URL: '/sitemap/'
urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemap_core}, name='django.contrib.sitemaps.views.sitemap'),
]