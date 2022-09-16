from django.db import models
from accounts.models import User
from buy.models import Buy
from free.models import Free

# class Accuse(models.Model):
#     content = body = models.TextField()
#     ID = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
#                                  null=False,
#                                  default="")# 글쓴이 
#     buyID = models.ForeignKey(Buy, on_delete=models.CASCADE, blank= True)#거래글
#     free = models.ForeignKey(Free, on_delete=models.CASCADE, blank= True )# 


# 신고,, > 게시글 신고는 게시글 에서 작성자 아이디 받아와서 유저 신고로
# 유저 신고는 