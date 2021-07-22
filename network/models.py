from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=False)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f"On {self.timestamp}, {self.poster} posts:\n{self.content}"

    def serialize(self):
        return {
            "poster": self.poster.username.capitalize(),
            "content": self.content,
            "timestamp": self.timestamp.strftime("%d %b %Y, %H:%M"),
            "likes": self.likes,
            "posterID": self.poster.id
        }

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} is now following {self.followed}"