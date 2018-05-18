# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Username,Danhmuc,Music,CredentialsModel,Forder,Musicid
# Register your models here.
admin.site.register(Danhmuc)
admin.site.register(Username)
admin.site.register(Music)
admin.site.register(CredentialsModel)
admin.site.register(Forder)
admin.site.register(Musicid)