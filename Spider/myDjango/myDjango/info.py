from django.shortcuts import render
 
def information(request):
    context = {}
    context['sname'] = '王霜霜'
    context['sno'] = '16219111324'
    context['sclass'] = '16计算机科学与技术三'
    return render(request, 'info.html', context)