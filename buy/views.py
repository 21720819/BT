from multiprocessing import context
from urllib import response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .forms import BuyModelform 
from .models import Buy
from chat.models import Chat
from accounts.models import User
import json, requests
from django.conf import settings


def p_category(request,category):
    categorys={'food':0,'necessity':1,'ott':2,'delivery':3}

    posts = Buy.objects.filter(category=categorys[category]).order_by('-id') #최신순 나열
    return render(request,'buy/home.html',{'category':category,'posts':posts})

def buyDetail(request, post_id):
    detail= get_object_or_404(Buy,id=post_id)
    # try:
    #     like = Bookmarks.objects.get(post=post_id)
    #     return render(request, 'buy/detail.html',{'detail':detail, 'like':like.lenght})
    # except:
    return render(request, 'buy/detail.html',{'detail':detail})

def buyCreate(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = BuyModelform(request.POST, request.FILES)
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.ID=get_object_or_404(User,id=user_id)
            # if (request.FILES['photo']):
            #     photo = request.FILES['photo']
            #     finished_form.photo = request.FILES['photo']
            finished_form.save()
            user.point+=30 # 포인트 30점
            user.setLevel()
            user.save()
            return redirect('buyHome')
    else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        form  = BuyModelform()
    return render(request,'buy/create.html', {'form':form})


def buyDelete(request, post_id):
    uid = request.user.id
    user = User.objects.get(id=uid)

    post = Buy.objects.get(pk=post_id)
    user.point -= post.join_count*10
    user.setLevel()
    user.save()
    post.delete()
    return redirect('buyHome')

def buyEdit(request, post_id):
    post = Buy.objects.get(id=post_id)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = BuyModelform(request.POST, request.FILES)
        if form.is_valid():

            
            print(form.cleaned_data)
            # {'name': '수정된 이름', 'image': <InMemoryUploadedFile: Birman_43.jpg 	(image/jpeg)>, 'gender': 'female', 'body': '수정된 내용'}
            post.title = form.cleaned_data['title']
            post.photo = form.cleaned_data['photo']
            post.body = form.cleaned_data['body']
            post.date = form.cleaned_data['date']
            post.price = form.cleaned_data['price']
            post.wpeople = form.cleaned_data['wpeople']
            post.location = form.cleaned_data['location']
            post.bocategorydy = form.cleaned_data['category']
            post.save()
            return redirect('../../../buy/detail/'+str(post.pk))
        
    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = BuyModelform(instance =post )
        context={
            'form':form,
            'writing':True,
            'now':'edit',

        }
        return render(request, 'buy/edit_post.html',context)


def addBookmark(request, post_id):
    detail = Buy.objects.get(pk=post_id)
    uid = request.user.id
    user = get_object_or_404(User, pk=uid)

    check_like_post = user.like_posts.filter(id=post_id)

    if request.method == 'POST':
        
        # try:
        #     mark = Bookmarks.objects.get(user=user, post=detail)
        #     mark.delete()
        # except:
        #     mark = Bookmarks()
        #     mark.post = detail
        #     mark.user = user
        #     mark.save()
        if check_like_post.exists():
            user.like_posts.remove(detail)
            detail.like_count -= 1
            detail.save()
        else:
            user.like_posts.add(detail)
            detail.like_count += 1
            detail.save()

    
    return redirect('buyDetail',str(post_id))


# def delBookmark(request, toilet_id):
#     post = Buy.objects.get(pk=toilet_id)
#     uid = request.user.id
#     user = get_object_or_404(User, pk=uid)

#     if request.method == 'POST':
#         mark = Bookmarks.objects.get(user=user, post=post)
#         mark.delete()
#         return redirect('profile/home.html', uid)





#거래 신청 함수
def join(request,post_id):
    post = get_object_or_404(Buy, pk=post_id)
    uid = request.user.id
    user = get_object_or_404(User, pk=uid)
    check_join_users = user.join_posts.filter(id=post_id)
    if check_join_users.exists():
        user.join_posts.remove(post)
        post.join_count -= 1
        post.save()
        user.point-=10
        user.setLevel()
        user.save()
    else:
        user.join_posts.add(post)
        post.join_count += 1
        post.save()
        user.point+=10
        user.setLevel()
        user.save()

    return redirect('buyDetail',str(post_id))

        # if check_like_post.exists():
        #     user.like_posts.remove(detail)
        #     detail.like_count -= 1
        #     detail.save()
        # else:
        #     user.like_posts.add(detail)
        #     detail.like_count += 1
        #     detail.save()

def removeUser(request, post_id):
    detail = Buy.objects.get(pk=post_id)
    uid = request.POST["username"]
    user = get_object_or_404(User, username=uid)

    check_like_post = user.join_posts.filter(id=post_id)

    if request.method == 'POST':
        
        # try:
        #     mark = Bookmarks.objects.get(user=user, post=detail)
        #     mark.delete()
        # except:
        #     mark = Bookmarks()
        #     mark.post = detail
        #     mark.user = user
        #     mark.save()
        if check_like_post.exists():
            user.join_posts.remove(detail)
            detail.join_count -= 1
            detail.save()
        # else:
        #     user.like_posts.add(detail)
        #     detail.like_count += 1
        #     detail.save()

    
    return redirect('auth',str(post_id))



 # 신청자 목록 보여주는 함수
def auth(request,post_id):
    post = get_object_or_404(Buy, pk=post_id)
    join_user = post.join_users.all()
    return render(request,  'buy/auth.html',{'join_users':join_user,  'post':post})   




#sendbird 그룹채널 생성
def createChannel(request, post_id):
    #sendbird 정보 가져오기
    application_id = settings.SENDBIRD_APPLICATION_ID
    sendbird_api_token = settings.SENDBIRD_API_TOKEN
    url = f"https://api-{application_id}.sendbird.com/v3/group_channels"
    api_headers = {"Api-Token": sendbird_api_token}
    post = get_object_or_404(Buy, pk=post_id)
    chat = Chat()
    writer_email = request.user.email #글쓴이도 추가
    join_users = post.join_users.all()
    join_user_list = []
    join_user_list.append(writer_email)
    for join_user in join_users:
         join_user_list.append(join_user.email)

    data = {
        "name": post.title,
        "inviter_id" : writer_email,
        "is_pulic" : False,
        "user_ids" : join_user_list,
    }
    
    res = requests.post(url, data=json.dumps(data), headers=api_headers)
    info = res.text
    parse = json.loads(info)
    channel_name = parse['name']
    channel_url = parse['channel_url']
    members = parse['members']
    member_list = []
    count = 0
    for i in range(len(members)):
        member_list.append(members[i]['user_id'])

    chat.channel_url = channel_url
    chat.channel_name = channel_name
    chat.emails = json.dumps(member_list)
    chat.count = count
    chat.save()

    post.check_chat = True
    post.save()

    return redirect('auth', str(post_id))


def map(request):
    # 아이디, 글제목 , 위도 경도 
    posts = Buy.objects.all()
    buy = []
    for post in posts:
        dict = {
            'id': post.id,
            'title' : post.title,
            'lat' : post.lat,
            'long' : post.long,
            'category' : post.category,
            'time' : post.join_count,
            'price' : post.price,
            'location' : post.location,
        }

        buy.append(dict)
    positionsJson = json.dumps(buy)

    return render(request, 'buy/map.html',{'positionsJson':positionsJson})

# # 검색
from django.db.models import Q # 필터조건 두가지 이상 적용하기 위함

def buyHome(request):
    sort = request.GET.get('sort','')
    order = '-id'
    if sort== 'date':
        order='-id'
    elif sort == 'likes':
        order = '-like_count'
    elif sort == 'lowprice':
        order = 'price'
    elif sort == 'highprice':
        order = '-price'


    post_list = Buy.objects.all().order_by(order) #최신순 나열
    context={}
    paginator = Paginator(post_list, 6) # 6개씩 잘라내기
    page = request.GET.get('page') # 페이지 번호 알아오기
    posts = paginator.get_page(page) # 페이지 번호 인자로 넘겨주기

    if 'q' in request.GET: # 검색어 있으면 
        query = request.GET.get('q')
        post_list = post_list.filter(Q (title__icontains=query) | Q (body__icontains=query) | Q(ID__username__icontains=query))
        paginator = Paginator(post_list, 6) # 6개씩 잘라내기
        page = request.GET.get('page') # 페이지 번호 알아오기
        posts = paginator.get_page(page) # 페이지 번호 인자로 넘겨주기
        
        if len(query)>1:
            context={
                'q' : query,
                'posts' : posts
            }
        
        return render(request,'buy/home.html',context)
    else:    
        context={
            'posts' : posts
        }
        
    
        return render(request,'buy/home.html',context)
    return render(request,'buy/home.html',context)


def searchResult(request):
    posts =None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        posts = Buy.objects.all().filter(Q (title__icontains=query) | Q (body__icontains=query))
    return render (request, 'buy/home.html', {'query':query, 'posts':posts})

