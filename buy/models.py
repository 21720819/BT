from django.db import models
from accounts.models import User
# Create your models here.

class Buy(models.Model):
    CATEGORY_CHOICES = [(0,'식재료'),(1,'생필품'),(2,'OTT'),(3,'배달')]
    title = models.CharField(max_length=200)
    body = models.TextField(blank=False,
                                 null=False,)
    writeDate = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(blank=False,
                                 null=False,)
    category = models.IntegerField(choices=CATEGORY_CHOICES,
                                 blank=False,
                                 null=False,
                                 default=0)
    wpeople = models.IntegerField(blank=False,
                                 null=False,)
    people = models.IntegerField(null=True,default=1)
    price = models.IntegerField(blank=False,
                                 null=False,)
    location=models.CharField(max_length=300)
    photo = models.ImageField(blank=True,null=True,upload_to='pur_photo')
    # lat = models.FloatField() #위도
    # long = models.FloatField() #경도
    ID = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
                                 null=False,
                                 default="")
    good = models.IntegerField(null=True,default=0)
    # joinID = ArrayField( 
    #      models.CharField(max_length=200)
    # )
    def __str__(self):
        return self.title
    