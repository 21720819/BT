from django.shortcuts import render,redirect,HttpResponse,resolve_url
from django.contrib import auth
from .forms import UserSignupform, UserLoginform
from .models import User
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

import json, requests

#sendbird 정보 가져오기
application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN
from django.contrib.auth.decorators import login_required

#sendbird 유저 등록 함수
def create_sendbird_user(user_id, nickname, profile_url=""):
    url = f"https://api-{application_id}.sendbird.com/v3/users"
    api_headers = {"Api-Token": sendbird_api_token}
    data = {
        "user_id": user_id,
        "nickname": nickname,
        "profile_url": profile_url,
    }
    res = requests.post(url, data=json.dumps(data), headers=api_headers)
    res_data = json.loads(res._content.decode("utf-8"))
    return json.dumps(res_data)



def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == "POST":
        singForm = UserSignupform(request.POST)
        # loginForm = UserLoginform()
        if request.POST["password"]==request.POST["password2"]:
            user = User.objects.create_user(
                email= request.POST['email'], password=request.POST['password'] ,username = request.POST['username']
            )
            create_sendbird_user(request.POST['email'],request.POST['username'])
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
        return redirect('home')
    else:
        return redirect('loginHome')
        
@csrf_exempt
def login(request):
    if request.method =="POST":
        loginForm = UserLoginform(request.POST)
        # singForm = UserSignupform()
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email = email, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return redirect('loginHome')
    else:
        return redirect('loginHome')

def loginHome(request):
    loginForm = UserLoginform()
    singForm = UserSignupform()
    return render(request, 'accounts/login.html',{'loginForm':loginForm , 'singForm':singForm})

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


from .forms import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'  # 템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'accounts/password_reset_done_fail.html')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'  # 템플릿을 변경하려면 이와같은 형식으로 입력


class UserPasswordResetConfirmView(PasswordResetConfirmView):

    form_class = CustomPasswordSetForm
    success_url = reverse_lazy('password_reset_complete')

    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


def custom_500_error(request):
    response = render(request, 'error/500.html')
    response.status_code = 500
    return response


def custom_404_error(request, exception):
    response = render(request, 'error/404.html')
    response.status_code = 404
    return response


def custom_400_error(request, exception):
    response = render(request, "error/400.html")
    response.status_code = 400
    return response


def e400(request):
    return render(request, 'error/400.html')

def e404(request):
    return render(request, 'error/404.html')

def e500(request):
    return render(request, 'error/500.html')

def loginerror(request):
    return render(request, 'error/login.html')


def delete(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('home')

# # from .models import Authentication

# # 네이버 SMS 인증
# class SmsSendView(View):
#     def send_sms(self, phone_number, auth_number):
#         timestamp = str(int(time.time() * 1000)) # sign  
#         headers = {
#             'Content-Type': "application/json; charset=UTF-8", # 네이버 참고서 차용
#             'x-ncp-apigw-timestamp': timestamp, # 네이버 API 서버와 5분이상 시간차이 발생시 오류
#             'x-ncp-iam-access-key': 'SdCSP6m7s7H4bba0QO3E',
#             'x-ncp-apigw-signature-v2': make_signature(timestamp) # utils.py 이용
#         }
#         body = {
#             "type": "SMS", 
#             "contentType": "COMM",
#             "from": "01092247763", # 사전에 등록해놓은 발신용 번호 입력, 타 번호 입력시 오류
#             "content": f"[바이투게더]인증번호:{auth_number}", # 메세지를 이쁘게 꾸며보자
#             "messages": [{"to": f"{phone_number}"}] # 네이버 양식에 따른 messages.to 입력
#         }
#         URL ='https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:292298761053:buytogether/messages' 
#         body = json.dumps(body)
#         requests.post(URL, headers=headers, data=body)
#         # 발송 URI 부분에는 아래 URL을 넣어주면 된다.
#         # 다만, 너무 길고 동시에 보안이슈가 있기에 별도로 분기해놓은 settings 파일에 넣어서 불러오는 것을 추천한다.
        
#     def post(self, request, username):
#         data = request.POST.get("phone_number")
#         input_mobile_num = data
#         auth_num = random.randint(10000, 100000) # 랜덤숫자 생성, 5자리로 계획하였다.
#         try:##인증ㅇ번호 발송
#             auth_mobile = User.objects.get(username=username)
#             auth_mobile.auth_number = auth_num
#             auth_mobile.phone_number = input_mobile_num
#             auth_mobile.save()
#             self.send_sms(phone_number=data, auth_number=auth_num)
#             # return JsonResponse({'message': '인증번호 발송완료'}, status=200)
#             return HttpResponse('인증번호 발송완료')
#         except User.DoesNotExist: # 인증요청번호 미 존재 시 DB 입력 로직 작성
#             User.objects.update_or_create(
#                 phone_number=input_mobile_num,
#                 auth_number=auth_num,
#             ).save()
#             self.send_sms(phone_number=input_mobile_num, auth_number=auth_num)
#             # return JsonResponse({'message': '인증번호 발송 및 DB 입력완료'}, status=200)
#             return HttpResponse('인증번호 발송완료 및 입력완료')





# # 네이버 SMS 인증번호 검증
# class SMSVerificationView(View):
#     def post(self, request, username):
#         data = request.POST.get("auth_number")
#         # phone_number = request.POST.get("phone_number")
#         try:
#             verification = User.objects.get(username=username)

#             if verification.auth_number == data:
#                 # return JsonResponse({'message': '인증 완료되었습니다.'}, status=200)
#                 return HttpResponse('인증완료')

#             else:
#                 # return JsonResponse({'message': '인증 실패입니다.'}, status=400)
#                 return HttpResponse('인증실패')

#         except User.DoesNotExist:
#                 return HttpResponse('인증실패')
#             # return JsonResponse({'message': '해당 휴대폰 번호가 존재하지 않습니다.'}, status=400)
    
#     # def get(self, request):
#     #     try:
#     #         phone_number = request.query_params['phone_number']
#     #         auth_number = request.query_params['auth_number']
#     #         result = Authentication.