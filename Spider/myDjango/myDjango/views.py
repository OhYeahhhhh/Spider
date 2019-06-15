from myApp.models import Movies,Weathers,Phones,Packages
from django.shortcuts import render
from django.core.paginator import Paginator

def m_showDB(request):
    movie_list = Movies.objects.all()
    
    return render(request, 'movie.html', {'movie_list': movie_list})

def w_showDB(request):
    city=request.GET.get('city','')
    if city=="":
        weather_list = Weathers.objects.all()
    else:
        weather_list = Weathers.objects.filter(wCity=city)
    return render(request, 'weather.html', {'weather_list': weather_list})

def p_showDB(request):
    phone_list = Phones.objects.all()

    paginator_obj=Paginator(phone_list,60)

    request_page_num=request.GET.get('page',1)
    page_obj=paginator_obj.page(request_page_num)
    total_page_number=paginator_obj.num_pages
    page_list=get_pages(int(total_page_number),int(request_page_num))
    return render(request, 'phone.html', {'page_obj':page_obj,'page_list':page_list})

def pa_showDB(request):
    package_list = Packages.objects.all()
    
    return render(request, 'package.html', {'package_list': package_list})

def get_pages(totalpage=1,current_page=1):
    WEB_DISPLAY_PAGE = 5
    front_offset = int(WEB_DISPLAY_PAGE / 2)
    if WEB_DISPLAY_PAGE % 2 == 1:
        behind_offset=front_offset
    else:
        behind_offset=front_offset -1

    if totalpage < WEB_DISPLAY_PAGE:
        return list(range(1,totalpage+1))
    elif current_page<=front_offset:
        return list(range(1,WEB_DISPLAY_PAGE+1))
    elif current_page>=totalpage-behind_offset:
        start_page=totalpage-WEB_DISPLAY_PAGE+1
        return list(range(start_page,totalpage+1))
    else:
        start_page=current_page-front_offset
        end_page=current_page+behind_offset
        return list(range(start_page,end_page+1))