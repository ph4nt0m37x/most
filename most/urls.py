"""
URL configuration for most project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mostApp.views import *

from mostApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name='index'),
    path("browse/", browse, name='browse'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('create/', create_post, name='create_post'),
    path('create/apply', create_app_post, name='create_app_post'),
    path('post/apply/<post_id>', apply, name='apply'),
    path('post/details/<post_id>', post, name='post'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/<user_id>', profile, name='profile'),
    path('collaborations/<user_id>', collaborations, name='collaborations'),
    path('bookmarks/', bookmarks, name='bookmarks'),
    path('bookmark/post/<post_id>', bookmark_post, name='bookmark_post'),
    path('bookmark/post/apply/<post_id>', bookmark_app_post, name='bookmark_app_post'),
    path('collaborate/<user_id>', collaborate, name='collaborate'),
    path('post/applied/', applied, name='applied'),
    path('search/', search, name='search'),
    path('browse/filter/', browse_filter, name='browse_filter'),
    path('browse/search/', browse_search, name='browse_search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
