from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField

STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    (2, "Archive"),
)

class Post(models.Model):
    title = models.CharField(max_length=64, unique=True)
    snippet = models.CharField(max_length=255)
    content = HTMLField()
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(
        upload_to="post",
        default= "post/sample.jpg",
    )
    author = models.ForeignKey(
        User,
        related_name="blog_posts",
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text