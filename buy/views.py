from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .forms import BuyModelform
from .models import Buy
from accounts.models import User


def buyHome(request):
    purchase = Buy.objects
    post_list = purchase.all().order_by('-id') #최신순 나열
    paginator = Paginator(post_list, 9) # 6개씩 잘라내기
    page = request.GET.get('page') # 페이지 번호 알아오기
    posts = paginator.get_page(page) # 페이지 번호 인자로 넘겨주기
    return render(request,'buy/home.html',{'purchase':purchase, 'posts':posts})


def p_category(request,category):
    categorys={'food':0,'necessity':1,'ott':2,'delivery':3}

    posts = Buy.objects.filter(category=categorys[category]).order_by('-id') #최신순 나열
    return render(request,'buy/category.html',{'category':category,'posts':posts})

def buyDetail(request, post_id):
    detail= get_object_or_404(Buy,id=post_id)
    return render(request, 'buy/detail.html',{'detail':detail})

def buyCreate(request):
    user_id =request.user.id
    if request.method == 'POST':
        form = BuyModelform(request.POST)
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.ID=get_object_or_404(User,id=user_id)
            finished_form.save()
            return redirect('buyHome')
    else:
        form  = BuyModelform()
    return render(request,'buy/create.html', {'form':form})


def buyDelete(request, post_id):
    post = Buy.objects.get(pk=post_id)
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