from django.shortcuts import get_object_or_404, redirect, render
import json, requests
from django.conf import settings

#sendbird 정보 가져오기
application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN

def chatHome(request):
    uid = request.user.email
    context = {'application_id':application_id, 'uid':uid}
    return render(request,'chat/chatHome.html',context)