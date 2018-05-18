# -*- coding: utf-8 -*-
from django import forms
from .models import Username
from .auth import createFolder
import re
from django.core.exceptions import ObjectDoesNotExist
class dangky(forms.Form):
    user = forms.CharField(label='Tài khoản ', max_length=40)
    email =forms.EmailField(label='Email')
    pw = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    pw2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    
    def clean_pw(self):
        if "pw" in self.cleaned_data:
            print "aaaaaaaaaaa"
            pw2 =self.data.get('pw2')
            pw =self.cleaned_data['pw']
            if pw == pw2:
                return pw
        raise forms.ValidationError('Mật khẩu không hợp lệ')
    def clean_user(self):
        user=self.cleaned_data['user']
        if not re.search(r'^\w+$',user):
            raise forms.ValidationError('Tên tài khoản không hợp lệ')
        try:
            Username.objects.get(user=user)
        except ObjectDoesNotExist:
            return user
        raise forms.ValidationError('User đã tồn tại!')
    def save(self):
        Username.objects.create(user=self.cleaned_data['user'], password=self.cleaned_data['pw'],email=self.cleaned_data['email'])
        createFolder(self.cleaned_data['user'])
        