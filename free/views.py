from django.shortcuts import render,redirect,get_object_or_404
from .forms import Freemodelform,CommentForm
from .models import Free
from accounts.models import User

def freeHome(request):
    posts= Free.objects.filter().order_by('-writeDate')

    return render(request,'free/freehome.html',{'posts':posts})

def freeCreate(request):
    user_id =request.user.id
    if request.method == 'POST':
        form = Freemodelform(request.POST)
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.ID=get_object_or_404(User,id=user_id)
            finished_form.save()
            return redirect('freeHome')
    else:
        form  = Freemodelform()
    return render(request,'free/freeCreate.html', {'form':form})

def freeDetail(request, free_id):
    detail = get_object_or_404(Free,pk=free_id)
    comment_form = CommentForm()
    return render(request,'free/detail.html',{'detail':detail,'comment_form':comment_form})

def create_comment(request, free_id):
    filled_form = CommentForm(request.POST)
    user_id =request.user.id

    if filled_form.is_valid():
        finished_form =filled_form.save(commit=False)
        finished_form.freeId=get_object_or_404(Free,pk=free_id)
        finished_form.ID=get_object_or_404(User,id=user_id)
        finished_form.save()

    return redirect('freeDetail',free_id)