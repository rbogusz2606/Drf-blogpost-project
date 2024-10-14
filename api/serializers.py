from rest_framework import serializers
from .models import BlogPost, Category, Comment, Like
from django.contrib.auth.models import User

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "published_date", "categories", "author", "like_count", "comment_count"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'password', 'email']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'author', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields = ['id', 'author', 'blog_post', 'created_at']