"""whoknows URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticSitemap

ADMIN_URL = settings.ADMIN_URL
sitemaps = {
    'static': StaticSitemap
}

urlpatterns = [
    path('', include('questions.urls', namespace='questions')),
    path('vote/', include('votes.urls', namespace='votes')),
    path('comment/', include('comments.urls', namespace='comments')),
    path('answer/', include('answers.urls', namespace='answers')),
    path('account/', include('account.urls', namespace='account')),
    path(ADMIN_URL, admin.site.urls),
    path('robots.txt',
         TemplateView.as_view(template_name="robots.txt",
                              content_type="text/plain"),
         name="robots_file"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
