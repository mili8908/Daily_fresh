from django.conf.urls import url
from apps.cart.views import CartInfoView, CartAddView, CartUpdateView, CartDeleteView


urlpatterns = [
    url(r'^$', CartInfoView.as_view(), name='show'),  # 显示购物车页面
    url(r'^add$', CartAddView.as_view(), name='add'),  # 购物车记录添加
    url(r'^update$', CartUpdateView.as_view(), name='update'),  # 购物车记录更新
    url(r'^delete$', CartDeleteView.as_view(), name='delete'),  # 购物车记录删除
]
