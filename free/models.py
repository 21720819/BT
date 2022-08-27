from django.db import models
from accounts.models import User

# Create your models here.
class Free(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    writeDate = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(blank=True,null=True,upload_to='free_photo')
    #작성자아이디
    ID = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
                                 null=False,
                                 default="")
    like_count = models.PositiveIntegerField(default=0)  
    # good = models.IntegerField()
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    body = models.TextField()
    writeDate = models.DateTimeField(auto_now_add=True)
    freeId = models.ForeignKey(Free, on_delete=models.CASCADE)
    #작성자아이디
    ID = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
                                 null=False,
                                 default="")
