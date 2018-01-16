from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def index(request):

    return render(request, 'index.html')


def goods_list(requset):

    return render(requset, 'list.html')


def goods_detail(requset):

    return render(requset, 'detail.html')