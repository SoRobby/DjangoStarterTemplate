"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('adminpanel/', include('apps.adminpanel.urls')),
    path('', include('apps.main.urls')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('', include('apps.feedback.urls', namespace='feedback')),
    path('', include('apps.profiles.urls', namespace='profiles')),

]

# CKEditor5 url pattern
urlpatterns.append(path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"))

# Sitemap url pattern
urlpatterns.append(path('sitemaps/', include('config.sitemaps')))

# Static medial files url pattern. Note: Should only be used in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Enable Django Debug Toolbar if configured
if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))

# Page error handlers
handler400 = 'apps.main.views.handle400'
handler403 = 'apps.main.views.handle403'
handler404 = 'apps.main.views.handle404'
handler500 = 'apps.main.views.handle500'
