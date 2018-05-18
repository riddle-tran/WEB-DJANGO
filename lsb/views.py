# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Danhmuc,Music,Musicid
from .formsdangky import dangky
from .formlogin import dangnhap
from django.http import HttpResponseRedirect,HttpResponse
from . import auth
# Create your views here.
def home(request):
    danhmuc=Danhmuc.objects.all()
    music=Music.objects.all()
    context = {
        'danhmuc':danhmuc,
        'music':music,
    }
    if request.method == 'POST':
        
        return HttpResponseRedirect("/nhaccuatui/")
    
    return render(request,'home.html',context)
def login(request):
    danhmuc=Danhmuc.objects.all()
    form = dangnhap()
    if request.method == 'POST':
        form=dangnhap(request.POST)
        if form.is_valid():
            request.session['user']=form.kt()
            return HttpResponseRedirect('/')
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
