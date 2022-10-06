from django.shortcuts import get_object_or_404,render,HttpResponse, redirect
from accounts.models import User
from buy.models import Buy
from accounts.forms import Smsform ,Smscheckform

def profileHome(request,user_name):
    user = get_object_or_404(User, username=user_name)
    p_post =  Buy.objects.filter(ID=user).order_by('-writeDate')
    likes = user.like_posts.all()
    joins = user.join_posts.all()

    return render(request, 'profile/home.html',{'user':user , 'p_post':p_post, 'likes':likes,'joins':joins})

def profileEdit(request,user_name):
    user = get_object_or_404(User, username=user_name)
    p_post =  Buy.objects.filter(ID=user).order_by('-writeDate')
    likes = user.like_posts.all()

    return render(request, 'profile/home.html',{'user':user , 'p_post':p_post, 'likes':likes})

#  sms 인증
# Python
import json, requests, time, random

# Django
from django.views import View
from django.http import JsonResponse
from .utils import make_signature
from django.contrib import messages

def sms(request, user_name): # 폼 출력 
    smsform  = Smsform()
    checksmsform = Smscheckform()
    return render(request,'profile/sms.html', {'smsform':smsform , 'checksmsform':checksmsform})

    # return render(request, 'profile/sms.html', {'username': user_name})

def send_sms(phone_number, auth_number):
    timestamp = str(int(time.time() * 1000)) # sign  
    headers = {
        'Content-Type': "application/json; charset=UTF-8", # 네이버 참고서 차용
        'x-ncp-apigw-timestamp': timestamp, # 네이버 API 서버와 5분이상 시간차이 발생시 오류
        'x-ncp-iam-access-key': 'SdCSP6m7s7H4bba0QO3E',
        'x-ncp-apigw-signature-v2': make_signature(timestamp) # utils.py 이용
    }
    body = {
        "type": "SMS", 
        "contentType": "COMM",
        "from": "01092247763", # 사전에 등록해놓은 발신용 번호 입력, 타 번호 입력시 오류
        "content": f"[바이투게더]인증번호:{auth_number}", # 메세지를 이쁘게 꾸며보자
        "messages": [{"to": f"{phone_number}"}] # 네이버 양식에 따른 messages.to 입력
    }
    URL ='https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:292298761053:buytogether/messages' 
    body = json.dumps(body)
    requests.post(URL, headers=headers, data=body)
        # 발송 URI 부분에는 아래 URL을 넣어주면 된다.
        # 다만, 너무 길고 동시에 보안이슈가 있기에 별도로 분기해놓은 settings 파일에 넣어서 불러오는 것을 추천한다.
    
def sendsms(request, username):
    if request.method=='POST':
        form = Smsform(request.POST)
        data = request.POST['phone_number']
        # data = request.POST.get["phone_number"]
        input_mobile_num = data
        auth_num = random.randint(10000, 100000) # 랜덤숫자 생성, 5자리로 계획하였다.
        try:##인증ㅇ번호 발송
            auth_mobile = User.objects.get(username=username)
            auth_mobile.auth_number = auth_num
            auth_mobile.phone_number = input_mobile_num
            auth_mobile.save()
            send_sms(phone_number=data, auth_number=auth_num)
            # return JsonResponse({'message': '인증번호 발송완료'}, status=200)
            messages.success(request, f"인증번호가 발송되었습니다. 인증번호를 입력해주세요")
        except User.DoesNotExist: # 인증요청번호 미 존재 시 DB 입력 로직 작성
            User.objects.update_or_create(
                phone_number=input_mobile_num,
                auth_number=auth_num,
            ).save()
            send_sms(phone_number=input_mobile_num, auth_number=auth_num)
            # return JsonResponse({'message': '인증번호 발송 및 DB 입력완료'}, status=200)
            # return HttpResponse('인증번호 발송완료 및 입력완료')
    
    return redirect('../../profile/'+username+'/sms')


def checksms(request,username):# 인증번호 확인
    
    if request.method == 'POST':
        form = Smscheckform(request.POST)
        if form.is_valid():
            data = request.POST.get("auth_number")
            # phone_number = request.POST.get("phone_number")
            try:
                verification = User.objects.get(username=username)

                if verification.auth_number == data:
                    # return JsonResponse({'message': '인증 완료되었습니다.'}, status=200)
                    messages.success(request, f"인증완료")
                    return redirect('../../profile/'+username)

                else:
                    # return JsonResponse({'message': '인증 실패입니다.'}, status=400)
                    messages.error(request, f"인증 실패")
                    return redirect('../../profile/'+username+'/sms')

            except User.DoesNotExist:
                    messages.error(request, f"인증 실패")
                    return redirect('../../profile/'+username+'/sms')
    

def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts =  Buy.objects.filter(ID=user).order_by('-writeDate')
    return render(request, 'profile/userprofile.html', {'user': user , 'posts' : posts})

# def report(request, username):
#     user = get_object_or_404(User, username=username)
