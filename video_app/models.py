# from django.db import models

# class Video(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     video_file = models.FileField(upload_to='videos/')

#     def __str__(self):
#         return self.title

from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.text}'
