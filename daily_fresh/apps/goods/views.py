from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def index(request):

    return render(request, 'goods/index.html')


def goods_list(requset):

    return HttpResponse('ok')


def goods_detail(requset):

    return HttpResponse('ok')
