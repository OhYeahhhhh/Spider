"""myDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from . import movieDB,weatherDB,phoneDB,info,views

urlpatterns = [
    url(r'^m_showDB/',views.m_showDB,name="m_showDB"), #显示数据库中电影数据

    url(r'^w_insertDB/',weatherDB.insertDB), #添加天气数据
    url(r'^w_showDB/',views.w_showDB,name="w_showDB"), #显示数据库中天气数据
    
    url(r'^p_insertDB/',phoneDB.insertDB),#添加手机数据
    url(r'^p_showDB/',views.p_showDB,name="p_showDB"), #显示数据库中手机数据

    url(r'^pa_showDB/',views.pa_showDB,name="pa_showDB"), #显示数据库中书包数据

    url(r'^info/',info.information,name="info"), #显示个人信息
]