from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import datetime
from django.db import transaction
from .models import Post
from .forms import PostForm


def blog_view(request):
    posts = Post.objects.all()
    return render(request, 'blog_base.html', {'posts': posts})


@transaction.atomic
def register_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = Post(title=form.cleaned_data['title'],
                        text=form.cleaned_data['text'],
                        image1=form.cleaned_data['image1'],
                        image2=form.cleaned_data['image2'],
                        image3=form.cleaned_data['image3'],
                        image4=form.cleaned_data['image4'])
            p.save()
    messages.success(request, "Post criado com sucesso!")
    return redirect(blog_view)


def add_post(request):
    return render(request, 'create_post.html')

def delete_post(request,id):
    p = Post.objects.get(pk=id)
    p.delete()
    messages.success(request, "Post eliminado com sucesso!")
    return redirect(blog_view)

def edit_post(request,id):
    p = Post.objects.get(pk=id)
    return render(request, 'edit_post.html',{"p":p})

@transaction.atomic
def save_post(request,id):
   if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = Post.objects.get(pk=id)
            p.title = form.cleaned_data['title']
            p.text = form.cleaned_data['text']
            p.image1 = form.cleaned_data['image1']
            p.image2 = form.cleaned_data['image2']
            p.image3 = form.cleaned_data['image3']
            p.image4 = form.cleaned_data['image4']
            p.save()
            messages.success(request, "Post editado com sucesso!")
            return redirect(blog_view)
