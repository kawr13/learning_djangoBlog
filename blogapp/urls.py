"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from blogapp.views import BlogListView, PostDetailView, PostSearchView
from .feeds import LatestPostsFeed


app_name = 'blogapp'


urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('tag/<str:tag_slug>/', BlogListView.as_view(), name='post_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='blog_detailed'),
    path('email_send/<int:post_id>/', PostDetailView.as_view(), name='email_send'),
    path('feed/', LatestPostsFeed(), name='blog_feed'),
    path('search/', PostSearchView.as_view(), name='post_search'),
]
