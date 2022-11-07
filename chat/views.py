from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
import json, requests
from django.conf import settings
from datetime import datetime
from .models import Chat
from time import time

application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN


def get_chat_members(channel_url):
    member_list= []
    emails = Chat.objects.get(channel_url = channel_url).emails.replace('[',"").replace(']',"").replace('"',"").replace(" ","").split(',')
    for email in emails :
        nick = User.objects.get(email=email).username
        profile_url = f"../profile/{nick}"
        dic = {'nick':nick, 'profile_url':profile_url}
        member_list.append(dic)

    return member_list


def set_profile_img(request):
     user_id = request.user.email #유저 이메일 지정
     url = f"https://api-{application_id}.sendbird.com/v3/users/{user_id}"
     api_headers = {"Api-Token": sendbird_api_token}
     level = User.objects.get(email=user_id).level
     if(level == 0) : 
       profiile_url = "../static/images/level0.png"
     elif (level == 1) : 
         profiile_url = "../static/images/level1.png"
     elif (level == 2) : 
         profiile_url = "../static/images/level2.png"    
     elif (level == 3) : 
         profiile_url = "../static/images/level3.png"    
     else :
        profiile_url = "../static/images/level4.png"    
        
     data ={
            'profile_url' : profiile_url,
     }

     res = requests.put(url, data= json.dumps(data), headers=api_headers)
     info = res.text
     parse = json.loads(info)
     #print(parse)


def chatHome(request):
    set_profile_img(request)
    user_id = request.user.email #유저 이메일 지정

    url = f"https://api-{application_id}.sendbird.com/v3/users/{user_id}/my_group_channels"
    api_headers = {"Api-Token": sendbird_api_token}
    
    data = {
        'order' : 'latest_last_message',
        'limit' : 100,
        'show_empty' : True,
    }

    res = requests.get(url, params=data, headers=api_headers)
    
    info = res.text
    parse = json.loads(info)
    channels = parse['channels'] #리스트

    chats = []
    
    for channel in channels : 
        channel_url = channel['channel_url']
        cover_url = channel['cover_url']
        chat_room_name = channel['name']
        member_count = channel['member_count']
        last = channel['last_message'] 
        try:
            pk = Chat.objects.get(channel_url = channel_url).pk
        except Chat.DoesNotExist:    
            pk = None
        if last is not None : 
            last_message = channel['last_message']['message']
            last_time = channel['last_message']['created_at']/1000
            time  = datetime.fromtimestamp(int(last_time)).strftime("%Y-%m-%d %H:%M")
        else :
            last_message = "메시지를 전송해 보세요."
            last_time = 0
            time  = 0
        dic = {'channel_url':channel_url, 'chat_room_name' : chat_room_name, 'last_message' : last_message, 'time' : time,'member_count' :member_count, 'application_id' : application_id, 'user_id' : user_id, 'pk' : pk , 'cover_url' : cover_url}
        chats.append(dic)

    context = {'chats' : chats, 'application_id' : application_id, 'user_id' : user_id}
    return render(request,'chat/chatHome.html', context)

def chatDetail(request, chat_id):
    set_profile_img(request)
    user_id = request.user.email 
    # 과거채팅 리스트 가져오기
    channel_type = "group_channels"
    message_ts = int(time()*1000) #현재시간을 unix 타임으로 변환
    channel_url = Chat.objects.get(id = chat_id).channel_url
    member_list = get_chat_members(channel_url)
    print(member_list)

    url =  f"https://api-{application_id}.sendbird.com/v3/{channel_type}/{channel_url}/messages"
    api_headers = {"Api-Token": sendbird_api_token}

    data = {
        'prev_limit' : 200,
        'next_limit' : 200,
        'message_ts' : message_ts,
    }
  
    res = requests.get(url, params=data, headers=api_headers)
    info = res.text
    parse = json.loads(info)
    #print(parse)
    try:
        chat_name = Chat.objects.get(channel_url = channel_url).channel_name
    except Chat.DoesNotExist:    
        chat_name = None
    try:
        member_count = Chat.objects.get(channel_url = channel_url).count
    except Chat.DoesNotExist:    
        member_count = None    

    messages = parse['messages']

    message_list = []
    
    for i in range(len(messages)):
        check_same = 0
        text = messages[i]['message']
        nickname = messages[i]['user']['nickname']
        sender_id = messages[i]['user']['user_id']
        sent_date_time = datetime.fromtimestamp(int(messages[i]['created_at']/1000))
        sent_time = sent_date_time.strftime("%H:%M")
        check_same_date = 1
        level = User.objects.get(email=sender_id).level

        sent_date = sent_date_time.strftime("%Y-%m-%d")
        if(i>=1 and message_list[i-1]['sent_date']==sent_date): #인덱스가 1보다 크고 이전 날짜와 같은 경우 0을 넣어라
            check_same_date = 0
        
        if (sender_id == user_id) :
            check_same = 1  #보낸 사람이랑 사용중인 사람이랑 같은 경우

        dic = {'text':text, 'nickname':nickname, 'check_same' : check_same, 'sent_date': sent_date, 'sent_time':sent_time, 'check_same_date':check_same_date, 'level':level }
        message_list.append(dic)

    last_date=0
    if(len(message_list)) :  
        last_date = message_list[-1]['sent_date']

    context = {'message_list' : message_list, 'channel_url':channel_url, 'application_id' : application_id, 'user_id' : user_id, 'last_date':last_date, 'chat_name':chat_name, 'member_count': member_count, 'member_list' : member_list}
   
    return render(request, 'chat/chatDetail.html', context)


def chatAI(request):
    return render(request, 'chat/chatAI.html')


