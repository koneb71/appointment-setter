from django.shortcuts import render


def landingpage(request):
    return render(request, 'landingpage/index.html')


def admin_dashboard(request):
    return render(request, 'portal/index.html')