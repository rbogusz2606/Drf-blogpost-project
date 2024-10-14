from django.contrib import admin
from .models import BlogPost, Category, Comment, Like

admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)