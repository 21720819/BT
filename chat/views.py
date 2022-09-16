from django.shortcuts import render
from django.conf import settings

#sendbird 정보 가져오기
application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN


def chatHome(request):
    return render(request,'chat/chatHome.html')