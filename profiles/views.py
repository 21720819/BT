from django.shortcuts import get_object_or_404,render
from accounts.models import User
from buy.models import Buy
from accounts.forms import smsform

def profileHome(request,user_name):
    user = get_object_or_404(User, username=user_name)
    p_post =  Buy.objects.filter(ID=user).order_by('-writeDate')
    likes = user.like_posts.all()

    return render(request, 'profile/home.html',{'user':user , 'p_post':p_post, 'likes':likes})

def sms(request, user_name):
    form 
    return render(request, 'profile/sms.html', {'username': user_name})