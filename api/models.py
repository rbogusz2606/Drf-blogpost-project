from django.db import models
import uuid
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self) -> str:
        return f" Autor: {self.author } , Post:{self.blog_post} , created at: {self.created_at}"

    
class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f" Autor: {self.author } , Post: {self.blog_post} , created at: {self.created_at}"