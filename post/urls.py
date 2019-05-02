"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from . import views

app_name = "post"
urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about_us, name="aboutUs"),
    path('category/<int:sub_id>/', views.sub_category, name="category"),
    path('category_all_posts/<int:sub_id>/', views.more_cat, name="more_cat"),
    path('popular/', views.popular, name="popular"),
    path('read/<int:post_id>/', views.read, name="read"),
    path('deleteComment/<int:comment_id>/', views.remove_comment, name="removeComment"),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name="edit_comment"),
    path('contact/', views.contact, name="contact"),
]
