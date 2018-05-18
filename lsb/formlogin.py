# -*- coding: utf-8 -*-
from django import forms
from .models import Username
import re
from django.core.exceptions import ObjectDoesNotExist
class dangnhap(forms.Form):
    user = forms.CharField(label='Tài khoản ', max_length=40)
    pw = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    def clean_pw(self):
        if "pw" in self.cleaned_data:
            pw =self.cleaned_data['pw']
            return pw
        raise forms.ValidationError('Mật khẩu không hợp lệ')
    def clean_user(self):
        user=self.cleaned_data['user']
        if not re.search(r'^\w+$',user):
            raise forms.ValidationError('Tên tài khoản không hợp lệ')
        try:
           a = Username.objects.get(user=self.cleaned_data['user'], password=self.data.get('pw'))
           return a.user
        except ObjectDoesNotExist:
            raise forms.ValidationError('User  hoặc password sai!')
    def kt(self):
        try:
           a = Username.objects.get(user=self.cleaned_data['user'], password=self.data.get('pw'))
           return a.user
        except ObjectDoesNotExist:
            raise forms.ValidationError('User  hoặc password sai!')