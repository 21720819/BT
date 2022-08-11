from django.shortcuts import get_object_or_404,render
from accounts.models import User
from buy.models import Buy

def profileHome(request,user_name):
    user = get_object_or_404(User, username=user_name)
    p_post =  Buy.objects.filter(ID=user).order_by('-writeDate')


    return render(request, 'profile/home.html',{'user':user , 'p_post':p_post})