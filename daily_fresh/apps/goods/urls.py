from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index$', views.index, name='index'),  # 主页
    url(r'^list$', views.goods_list, name='list'),  # 商品列表
    url(r'^detail$', views.goods_detail, name='detail')  # 商品详情
]
