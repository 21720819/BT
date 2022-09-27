from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .forms import BuyModelform
from .models import Buy
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
        form = BuyModelform(request.POST)
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.ID=get_object_or_404(User,id=user_id)
            if request.FILES['photo']:
                photo = request.FILES['photo']
                finished_form.photo = photo
            user.point+=30 # 포인트 30점
            user.setLevel()
            user.save()
            finished_form.save()
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
            post.title = form.cleaned_data['name']
            post.photo = form.cleaned_data['image']
            post.body = form.cleaned_data['body']
            post.date = form.cleaned_data['date']
            post.price = form.cleaned_data['price']
            post.wpeople = form.cleaned_data['wpeople']
            post.location = form.cleaned_data['location']
            post.bocategorydy = form.cleaned_data['category']
            post.save()
            return redirect('/detail/'+str(post.pk))
        
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

#sendbird 정보 가져오기
application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN

#sendbird 그룹채널 생성
def createChannel(request, post_id):
    url = f"https://api-{application_id}.sendbird.com/v3/group_channels"
    api_headers = {"Api-Token": sendbird_api_token}
    post = get_object_or_404(Buy, pk=post_id)
    uid = request.user.email #글쓴이도 추가
    join_users = post.join_users.all()
    join_user_list = []
    join_user_list.append(uid)
    for join_user in join_users:
         join_user_list.append(join_user.email)

    data = {
        "name": post.title,
        "is_pulic" : False,
        "user_ids" : join_user_list,
    }
    
    requests.post(url, data=json.dumps(data), headers=api_headers)
    return redirect('auth', str(post_id))

 # 신청자 목록 보여주는 함수
def auth(request,post_id):
    post = get_object_or_404(Buy, pk=post_id)
    join_user = post.join_users.all()
    return render(request,  'buy/auth.html',{'join_users':join_user,  'post_id':post_id})   

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
        }

        buy.append(dict)
    positionsJson = json.dumps(buy)

    return render(request, 'buy/map.html',{'positionsJson':positionsJson})

# # 검색
from django.db.models import Q # 필터조건 두가지 이상 적용하기 위함

def buyHome(request):
    post_list = Buy.objects.all().order_by('-id') #최신순 나열
    context={}
    # paginator = Paginator(post_list, 9) # 6개씩 잘라내기
    # page = request.GET.get('page') # 페이지 번호 알아오기
    # posts = paginator.get_page(page) # 페이지 번호 인자로 넘겨주기
    if 'q' in request.GET: # 검색어 있으면 
        query = request.GET.get('q')
        posts = Buy.objects.all().filter(Q (title__icontains=query) | Q (body__icontains=query))
        if len(query)>1:
            context={
                'q' : query,
                'posts' : posts
            }
        return render(request,'buy/home.html',context)
    else:    
        context={
            'posts' : post_list
        }
        return render(request,'buy/home.html',context)


def searchResult(request):
    posts =None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        posts = Buy.objects.all().filter(Q (title__icontains=query) | Q (body__icontains=query))
    return render (request, 'buy/home.html', {'query':query, 'posts':posts})


# from django.contrib import messages
# from django.views.generic import View, ListView

# class NoticeListView(ListView):
#     model = Buy
#     paginate_by = 15
#     template_name = 'buy/home.html'  #DEFAULT : <app_label>/<model_name>_list.html
#     context_object_name = 'notice_list'        #DEFAULT : <app_label>_list

#     def get_queryset(self):
#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         notice_list = Buy.objects.order_by('-id') 
        
#         if search_keyword :
#             if len(search_keyword) > 1 :
#                 if search_type == 'all':
#                     search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (body__icontains=search_keyword) | Q (ID__user_id__icontains=search_keyword))
#                 elif search_type == 'title_content':
#                     search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (body__icontains=search_keyword))
#                 elif search_type == 'title':
#                     search_notice_list = notice_list.filter(title__icontains=search_keyword)    
#                 elif search_type == 'content':
#                     search_notice_list = notice_list.filter(body__icontains=search_keyword)    
#                 elif search_type == 'writer':
#                     search_notice_list = notice_list.filter(ID__user_id__icontains=search_keyword)

#                 # if not search_notice_list :
#                 #     messages.error(self.request, '일치하는 검색 결과가 없습니다.')
#                 return search_notice_list
#             else:
#                 messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
#         return notice_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)

#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index

#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range

#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         # notice_fixed = Buy.objects.filter(top_fixed=True).order_by('-id')

#         if len(search_keyword) > 1 :
#             context['q'] = search_keyword
#         context['type'] = search_type
#         # context['notice_fixed'] = notice_fixed

#         return context
