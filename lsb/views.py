# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Danhmuc,Music,Musicid,Forder
from .formsdangky import dangky
from .formlogin import dangnhap
from django.http import HttpResponseRedirect,HttpResponse
from . import api
from .formUpdate import UploadFileForm
from .lsb_hiding import recover_lsb_watermark
import os
# Create your views here.
def home(request):
    danhmuc=Danhmuc.objects.all()
    music=Music.objects.all()
    context = {
        'danhmuc':danhmuc,
        'music':music,
    }
    if request.method == 'POST':
        if 'user' in request.session:
            user = request.session['user']
            id =request.POST.get('id')
            tenbai=(Music.objects.get(ma=id)).tenbai
            forder=(Forder.objects.get(user=user)).ma
            api.downloadFile(id,tenbai,user,forder)
            return HttpResponseRedirect("/nhaccuatui")
        else:
            return HttpResponseRedirect("/login")
    
    return render(request,'home.html',context)
def login(request):
    danhmuc=Danhmuc.objects.all()
    form = dangnhap()
    if request.method == 'POST':
            form=dangnhap(request.POST)
            if form.is_valid():
                request.session['user']=form.kt()
                return HttpResponseRedirect('/')
    if request.method == 'GET':            
        if request.GET.get('dangki'):
                return HttpResponseRedirect('/dangki')
    context = {
        'danhmuc':danhmuc,
        'form':form,
    }
    return render(request,'login.html',context)



def logout(request):
    del request.session['user']
    return HttpResponseRedirect('/')

def nhaccuatui(request):
    user= request.session['user']
    danhmuc=Danhmuc.objects.all()
    music=Musicid.objects.filter(user=user)
    context = {
        'danhmuc':danhmuc,
        'music':music,
    }
    return render(request,'nhaccuatui.html',context)

def dangki(request):
    danhmuc=Danhmuc.objects.all()
    form = dangky()
    if request.method == 'POST':
        form=dangky(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
    context = {
        'danhmuc':danhmuc,
        'form':form,
    }
    return render(request,'dangki.html',context)
def list(request):
    api.listFiles()
    return HttpResponseRedirect('/')
def kiemtra(request):
    danhmuc=Danhmuc.objects.all()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            a=request.FILES['file']
            upload(a)
            filepath="upload/" + a.name
            b=recover_lsb_watermark(filepath)
            os.remove(filepath)
            context = {
                'danhmuc':danhmuc,
                'code':b,
            }
            return render(request, 'kiemtra.html', context)
        else:
            form = UploadFileForm()
            context = {
                'danhmuc':danhmuc,
                'code':"Thất bại! Hãy chọn file wav lại",
                'form':form,
            }
            return render(request, 'kiemtra.html', context)
 
    form = UploadFileForm()
    context = {
                'danhmuc':danhmuc,
                'code':"Chọn file wav",
                'form':form,
            }
    return render(request, 'kiemtra.html', context)
def update(request):
    danhmuc=Danhmuc.objects.all()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            a=request.FILES['file']
            upload(a)
            filepath="upload/" + a.name
            os.remove(filepath)
            context = {
                'danhmuc':danhmuc,
                'code':"upload thành công",
            }
            return render(request, 'update.html', context)
        else:
            form = UploadFileForm()
            context = {
                'danhmuc':danhmuc,
                'code':"Thất bại! Hãy chọn file wav lại",
                'form':form,
            }
            return render(request, 'update.html', context)
 
    form = UploadFileForm()
    context = {
                'danhmuc':danhmuc,
                'code':"Chọn file wav",
                'form':form,
            }
    return render(request, 'update.html', context)
def upload(f): 
    filepath="upload/" + f.name
    file = open(filepath, 'wb+') 
    for chunk in f.chunks():
        file.write(chunk)