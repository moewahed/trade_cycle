from django.db import models

from user.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, related_name='blog', on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_at']


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_at']
