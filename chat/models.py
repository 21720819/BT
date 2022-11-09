from django.db import models
# Create your models here.

class Chat(models.Model):
    channel_url = models.CharField(
        max_length=200,
        unique=True,
    )
    channel_name = models.CharField(max_length=200)
    emails = models.TextField(null = True)
    count =  models.PositiveIntegerField(default=0)
    post_num = models.PositiveIntegerField(default=0)
    def __str__(self):
        return "<%d %s>" %(self.pk, self.channel_url)
    