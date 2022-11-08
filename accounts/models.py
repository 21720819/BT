from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.core.validators import validate_email
from .validators import validate_symbols
      

# from buy.models import Buy
class User(AbstractUser):    
    # def validate_email(value):
    #     if ("@ynu.ac.kr" not in value):
    #         raise ValidationError(
    #             _('영남대학교 이메일을 사용해야합니다.%(value)는 영남대 이메일이 아닙니다.'),
    #             params={'value':value},
    #             )
  
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
    join_posts = models.ManyToManyField('buy.Buy', blank=True, related_name='join_users') #참가신청한 글 

    phone_number = models.CharField('휴대폰 번호', max_length=30, unique = True, null=True, blank=True)
    auth_number = models.CharField('인증번호', max_length=30)

    def __str__(self):
        return "<%d %s>" %(self.pk, self.email)

    def setLevel(self):
        if (self.level == 0)and (self.point>=100):
            self.level =1
            self.point = self.point-100
        if (self.level == 1)and (self.point>=300):
            self.level =2
            self.point = self.point-300            
        if (self.level == 2)and (self.point>=1000):
            self.level =3
            self.point = self.point-1000

        return self.level

# class Authentication(models.Model):
#     phone_number = models.CharField('휴대폰 번호', max_length=30)
#     auth_number = models.CharField('인증번호', max_length=30)

#     class Meta:
#         db_table = 'authentications' # DB 테이블명
#         verbose_name_plural = "휴대폰인증 관리 페이지" # Admin 페이지에서 나타나는 설명