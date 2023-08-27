# Project's apps sitemaps
from apps.main.sitemaps import MainStaticSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

# Sitemap URLS
# https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/

# Dictionary of project sitemaps
sitemap_main = {'sitemap': MainStaticSitemap}

# Sitemap base URL: '/sitemap/'
urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemap_main}, name='django.contrib.sitemaps.views.sitemap'),
]