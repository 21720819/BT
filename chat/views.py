from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
import json, requests
from django.conf import settings
from datetime import datetime
from .models import Chat
from buy.models import Buy
from time import time
from django.contrib.auth.decorators import login_required

application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN


def outChannel(request, chat_id):
    user_id = request.user.email #유저 이메일 지정
    url = f"https://api-{application_id}.sendbird.com/v3/users/{user_id}/my_group_channels/leave"
    api_headers = {"Api-Token": sendbird_api_token}
    data = {
            }
    res = requests.put(url, data= json.dumps(data), headers=api_headers)
    chat=Chat.objects.get(pk = chat_id)
    # 참가자 리스트 불러오기
    try:
        emails = Chat.objects.get(pk = chat_id).emails.replace('[',"").replace(']',"").replace('"',"").replace(" ","").split(',')
    except :
        emails = None
    if(emails) :
        emails.remove(user_id)
        chat.count-=1
        chat.emails=json.dumps(emails)
        chat.save()

    info = res.text
    parse = json.loads(info)
    #print(parse)
    return redirect('chatHome')

def get_chat_members(request, channel_url):
    user_id = request.user.email #유저 이메일 지정
    member_list= []
    try:
        emails = Chat.objects.get(channel_url = channel_url).emails.replace('[',"").replace(']',"").replace('"',"").replace(" ","").split(',')
    except :
        emails = None
    if(emails) :
        for email in emails :
            try:
                nick = User.objects.get(email=email).username 
                level =  User.objects.get(email=email).level 
            except:
                nick = None
                level = None
            if (nick):
                    if (email == user_id) :      
                        profile_url = f"../profile/{nick}"
                        dic = {'nick':nick, 'profile_url':profile_url, 'level' : level}  
                    else :
                        profile_url = f"../profile/userprofile/{nick}"
                        dic = {'nick':nick, 'profile_url':profile_url, 'level' : level}  


                    member_list.append(dic)
        return member_list


def set_chatImg(channel_url, post_id) :
    url = f"https://api-{application_id}.sendbird.com/v3/group_channels/{channel_url}"
    api_headers = {"Api-Token": sendbird_api_token}
    try:
        #post = get_object_or_404(Buy, pk=post_id)
        post = User.objects.get(empkail=post_id).username 
        if(post) : 
                try:      
                    cover_url = post.photo.url
                except: 
                    if post.category == 0:
                        cover_url = "../static/images/food3.jpg"
                    elif post.category == 1:
                        cover_url = "../static/images/food1.jpg"
                    elif post.category == 2:
                        cover_url = "../static/images/ott1.jpg"
                    else :
                        cover_url = "../static/images/delivery1.jpg"
                data ={
                        'cover_url' : cover_url,
                    }     
                res = requests.put(url, data= json.dumps(data), headers=api_headers)
                info = res.text
                parse = json.loads(info)
                #print(parse)    
    except:
        post = None


def set_profileImg_nick(request):
     user_id = request.user.email #유저 이메일 지정
     url = f"https://api-{application_id}.sendbird.com/v3/users/{user_id}"
     api_headers = {"Api-Token": sendbird_api_token}
     level = User.objects.get(email=user_id).level
     if(level == 0) : 
       profile_url = "../static/images/level0.png"
     elif (level == 1) : 
         profile_url = "../static/images/level1.png"
     elif (level == 2) : 
         profile_url = "../static/images/level2.png"    
     elif (level == 3) : 
         profile_url = "../static/images/level3.png"    
     else :
        profile_url = "../static/images/level4.png"    
     nick = User.objects.get(email=user_id).username
        
     data ={
            'profile_url' : profile_url,
            'nickname' : nick
     }

     res = requests.put(url, data= json.dumps(data), headers=api_headers)
     info = res.text
     parse = json.loads(info)
     #print(parse)

@login_required(login_url='/accounts/login/')
def chatHome(request):
    set_profileImg_nick(request)
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
        last = channel['last_message'] 
        
        try:
            pk = Chat.objects.get(channel_url = channel_url).pk
            post_num = Chat.objects.get(pk = pk).post_num
            set_chatImg(channel_url, post_num)
            mem_list = get_chat_members(request, channel_url)
        except Chat.DoesNotExist:    
            pk = None
            mem_list = None
        if last is not None : 
            last_message = channel['last_message']['message']
            last_time = channel['last_message']['created_at']/1000
            time  = datetime.fromtimestamp(int(last_time)).strftime("%Y-%m-%d %H:%M")
        else :
            last_message = "메시지를 전송해 보세요."
            last_time = 0
            time  = 0
        if  (mem_list):
            mem_count = len(mem_list)
            dic = {'channel_url':channel_url, 'chat_room_name' : chat_room_name, 'last_message' : last_message, 'time' : time,'mem_count' :mem_count, 'application_id' : application_id, 'user_id' : user_id, 'pk' : pk , 'cover_url' : cover_url}
            chats.append(dic)

    context = {'chats' : chats, 'application_id' : application_id, 'user_id' : user_id}
    return render(request,'chat/chathome.html', context)

def chatDetail(request, chat_id):
    set_profileImg_nick(request)
    user_id = request.user.email 
    # 과거채팅 리스트 가져오기
    channel_type = "group_channels"
    message_ts = int(time()*1000) #현재시간을 unix 타임으로 변환
    channel_url = Chat.objects.get(id = chat_id).channel_url
    post_num = Chat.objects.get(id = chat_id).post_num
    try:
        post_completed = Buy.objects.get(id=post_num).complete
    except:
        post_completed = -1
    member_list = get_chat_members(request, channel_url)
    member_count = len(member_list)

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

    messages = parse['messages']

    message_list = []
    
    for i in range(len(messages)):
        check_same = 0
        text = messages[i]['message']
        sender_id = messages[i]['user']['user_id']
        try:
             nickname =  User.objects.get(email=sender_id).username 
        except:
            nickname = messages[i]['user']['nickname']
        sent_date_time = datetime.fromtimestamp(int(messages[i]['created_at']/1000))
        sent_time = sent_date_time.strftime("%H:%M")
        check_same_date = 1
        profile_url = f"/profile/userprofile/{nickname}"
        try:
            level = User.objects.get(email=sender_id).level
        except :
            level = -1

        sent_date = sent_date_time.strftime("%Y-%m-%d")
        if(i>=1 and message_list[i-1]['sent_date']==sent_date): #인덱스가 1보다 크고 이전 날짜와 같은 경우 0을 넣어라
            check_same_date = 0
        
        if (sender_id == user_id) :
            check_same = 1  #보낸 사람이랑 사용중인 사람이랑 같은 경우

        dic = {'text':text, 'nickname':nickname, 'check_same' : check_same, 'sent_date': sent_date, 'sent_time':sent_time, 'check_same_date':check_same_date, 'level':level, 'profile_url':profile_url }
        message_list.append(dic)

    last_date=0
    if(len(message_list)) :  
        last_date = message_list[-1]['sent_date']

    context = {'message_list' : message_list, 'channel_url':channel_url, 'application_id' : application_id, 'user_id' : user_id, 'last_date':last_date, 'chat_name':chat_name, 'member_list' : member_list, 'member_count':member_count, 'post_num':post_num, 'post_completed':post_completed, 'chat_id':chat_id}
   
    return render(request, 'chat/chatDetail.html', context)

@login_required(login_url='/accounts/login/')
def chatAI(request):
    return render(request, 'chat/chatAI.html')


