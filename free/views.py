from django.shortcuts import render,redirect,get_object_or_404
from .forms import Freemodelform,CommentForm
from .models import Free
from accounts.models import User
from django.contrib.auth.decorators import login_required

def freeHome(request):
    posts= Free.objects.filter().order_by('-writeDate')

    return render(request,'free/freehome.html',{'posts':posts})

@login_required(login_url='/accounts/login/')
def freeCreate(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = Freemodelform(request.POST)
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.ID=get_object_or_404(User,id=user_id)
            finished_form.save()
            user.point+=5 # 포인트 5점 
            user.setLevel()
            user.save()
            return redirect('freeHome')
    else:
        form  = Freemodelform()
    return render(request,'free/freeCreate.html', {'form':form})

@login_required(login_url='/accounts/login/')
def freeDetail(request, free_id):
    detail = get_object_or_404(Free,pk=free_id)
    comment_form = CommentForm()
    return render(request,'free/detail.html',{'detail':detail,'comment_form':comment_form})

def create_comment(request, free_id):
    filled_form = CommentForm(request.POST)
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    if filled_form.is_valid():
        finished_form =filled_form.save(commit=False)
        finished_form.freeId=get_object_or_404(Free,pk=free_id)
        finished_form.ID=get_object_or_404(User,id=user_id)
        finished_form.save()
        user.point+=1 # 포인트 1점 
        user.setLevel()
        user.save()

    return redirect('freeDetail',free_id)

def freeDelete(request, free_id):
    post = Free.objects.get(pk=free_id)
    post.delete()
    return redirect('freeHome')

def freeEdit(request, free_id):
    post = Free.objects.get(id=free_id)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = Freemodelform(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            # {'name': '수정된 이름', 'image': <InMemoryUploadedFile: Birman_43.jpg 	(image/jpeg)>, 'gender': 'female', 'body': '수정된 내용'}
            post.title = form.cleaned_data['title']
            post.photo = form.cleaned_data['photo']
            post.body = form.cleaned_data['body']
            post.save()
            return redirect('../../detail/'+str(post.pk))
        
    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = Freemodelform(instance =post )
        context={
            'form':form,
            'writing':True,
            'now':'edit',
        }
        return render(request, 'free/Edit_free.html',context)

def freeLike(request, free_id):
    detail = Free.objects.get(pk=free_id)
    uid = request.user.id
    user = get_object_or_404(User, pk=uid)

    check_like_post = user.like_frees.filter(id=free_id)

    if request.method == 'POST':
        if check_like_post.exists():
            user.like_frees.remove(detail)
            detail.like_count -= 1
            detail.save()
        else:
            user.like_frees.add(detail)
            detail.like_count += 1
            detail.save()

    
    return redirect('freeDetail',str(free_id))

