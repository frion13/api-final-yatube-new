from django.contrib import admin

from .models import Comment, Follow, Group, Post

admin.site.register((Post, Comment, Group, Follow))
