from django.contrib import sitemaps
from django.urls import reverse


class MainStaticSitemap(sitemaps.Sitemap):
    """
    Sitemap generator for static pages of the app.

    Attributes:
    - changefreq: This indicates how frequently the content of the page is likely to change.
    - priority: This indicates the priority of the page relative to other pages on your site. Valid values range from 0.0 to 1.0.

    Sources:
    - https://docs.djangoproject.com/en/4.0/ref/contrib/sitemaps/#sitemap-class-reference
    """
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        """
        List all static pages of the app.
        """
        return ['home', ]

    def location(self, item):
        """
        location method: This method takes an object returned by items() and returns its URL.
        In this case, it's simply using Django's reverse() function to find the URL for each view.
        """
        return reverse(item)
