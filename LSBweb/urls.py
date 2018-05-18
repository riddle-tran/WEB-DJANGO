"""LSBweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from lsb import views as viewslsb
from lsb import auth as views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', viewslsb.home),
    url(r'^123$', viewslsb.logout),
    url(r'^login$', viewslsb.login),
    url(r'^dangki$', viewslsb.dangki ),
    url(r'^nhaccuatui$',viewslsb.nhaccuatui ),
    url(r'^logout$', viewslsb.logout),
    url(r'oauth2callback$',views.oauth2callback),
    url(r'oauth/$',views.oauth),
    url(r'^index/$', views.index),

]
