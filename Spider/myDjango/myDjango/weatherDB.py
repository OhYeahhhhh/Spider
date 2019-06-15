import MySQLdb
import urllib.request
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from myApp.models import Weathers
from django.http import HttpResponse
from django.shortcuts import render

def getData(request):
    
    headers={"User-Agent":"Mozilla/5.0(Windows;U;Windows NT 6.0 x64;en-US;rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
    cityCode={"台州":"101210601","温州":"101210701","宁波":"101210401","杭州":"101210101","绍兴":"101210507"}
    city=request.GET.get('city','')

    if city not in cityCode.keys():
        return 0
    else:
        url="http://www.weather.com.cn/weather/"+cityCode[city]+".shtml"
        req=urllib.request.Request(url,headers=headers)
        data=urllib.request.urlopen(req)
        data=data.read()
        dammit=UnicodeDammit(data,["utf-8","gbk"])
        data=dammit.unicode_markup
        soup=BeautifulSoup(data,"lxml")
        lis=soup.select("ul[class='t clearfix'] li")
        date=[]
        weather=[]
        temp=[]
        for li in lis:
            date.append(li.select('h1')[0].text)
            weather.append(li.select('p[class="wea"]')[0].text)
            if len(li.select('p[class="tem"] span'))==0:
                temp.append(li.select('p[class="tem"] i')[0].text)
            else:
                temp.append(li.select('p[class="tem"] span')[0].text+"/"+li.select('p[class="tem"] i')[0].text)
        return date,weather,temp

def insertDB(request):
    city=request.GET.get('city','')
    if getData(request)==0:
        return HttpResponse("<p>City cannot be found</p>")
    else:
        date,weather,temp=getData(request)
        for i in range(0,len(date)):
            weatherDB=Weathers(wCity=city,wDate=date[i],wWeather=weather[i],wTemp=temp[i])
            weatherDB.save()
        return HttpResponse("<p>数据添加成功！</p>")