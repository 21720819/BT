from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from .forms import UserSignupform, UserLoginform
from .models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == "POST":
        form = UserSignupform(request.POST)
        if request.POST["password"]==request.POST["password2"]:
            user = User.objects.create_user(
                email= request.POST['email'], password=request.POST['password'] ,username = request.POST['username']
            )
            user.is_active = False
            user.save()
            current_site = get_current_site(request) 
            # localhost:8000
            message = render_to_string('accounts/user_activate_email.html',                         
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = "[buytogether] 회원가입 인증 메일입니다."
            user_email = user.email
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse( #페이지 새로만드는것도 괜찮을듯
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )

            # auth.login(request,user)
            return redirect('home')
        return render(request,'accounts/signup.html',{'form':form})
    else:
        form = UserSignupform()
    return render(request, 'accounts/signup.html',{'form':form})

def login(request):
    if request.method =="POST":
        form = UserLoginform(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email = email, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            render(request, 'accounts/bad_login.html',{'form':form})
    else:
        form = UserLoginform()
        return render(request, 'accounts/login.html',{'form':form})

def logout(request):
    auth.logout(request)
    return redirect('home')


def activate(request, uid64, token):

    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('home')
    else:
        return HttpResponse('비정상적인 접근입니다.')