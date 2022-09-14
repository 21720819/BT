from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# from buy.models import Buy
class User(AbstractUser):    
#     # blank=True: 폼(입력양식)에서 빈채로 저장되는 것을 허용, DB에는 ''로 저장
#     # CharField 및 TextField는 blank=True만 허용, null=True 허용 X # null=True: DB에 NULL로 저장
#     nickname = models.CharField(max_length=50)
    email = models.EmailField(
        blank=False, 
        null=False,
        unique=True,
        error_messages={
            'unique': "이미 존재하는 ID 입니다.",
        },
        )
    username = models.CharField(
        max_length=30, 
        unique=True,
        error_messages={
            'unique': "이미 존재하는 닉네임입니다.",
        },)
    level = models.IntegerField(null=True,default=0)
    point = models.IntegerField(null=True,default=0)
    first_name = None
    last_name = None

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']#superuser 만들때 사용되는 필드 

    like_posts = models.ManyToManyField('buy.Buy', blank=True, related_name='like_users')
    like_frees = models.ManyToManyField('free.Free', blank=True, related_name='freeLike_users')
    join_posts = models.ManyToManyField('buy.Buy', blank=True, related_name='join_users')

    phone_number = models.CharField('휴대폰 번호', max_length=30)
    auth_number = models.CharField('인증번호', max_length=30)

    def __str__(self):
        return "<%d %s>" %(self.pk, self.email)

# class Authentication(models.Model):
#     phone_number = models.CharField('휴대폰 번호', max_length=30)
#     auth_number = models.CharField('인증번호', max_length=30)

#     class Meta:
#         db_table = 'authentications' # DB 테이블명
#         verbose_name_plural = "휴대폰인증 관리 페이지" # Admin 페이지에서 나타나는 설명