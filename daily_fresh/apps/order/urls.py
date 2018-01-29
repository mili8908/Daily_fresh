from django.conf.urls import url
from apps.order.views import OrderPlaceView, OrderCommitView, OrderPayView, OrderCheckView


urlpatterns = [
    url(r'^place$', OrderPlaceView.as_view(), name='place'),  # 提交订单页面
    url(r'^commit$', OrderCommitView.as_view(), name='commit'),  # 生成订单
    url(r'^pay$', OrderPayView.as_view(), name='pay'),  # 订单支付
    url(r'^check$', OrderCheckView.as_view(), name='check'),  # 订单支付结果查询

]