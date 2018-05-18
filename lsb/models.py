# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField

class CredentialsModel(models.Model):
    id = models.AutoField(primary_key=True)
    cred = CredentialsField()
# Create your models here.
class Username(models.Model):
    user = models.CharField(max_length=40, primary_key=True)
    password =  models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
class Forder(models.Model):
    user = models.CharField(max_length=40, primary_key=True)
    ma=models.CharField(max_length=100)
class Music(models.Model):
    tenbai = models.CharField(max_length=250)
    ma = models.CharField(max_length=100)
    def __str__(self):
        return self.tenbai

class Musicid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=40)
    tenbai = models.CharField(max_length=250)
    ma= models.CharField(max_length=100)
class Danhmuc(models.Model):
    ten =models.CharField(max_length=50)
    url =models.CharField(max_length=50)