from django.conf.urls import url
from .views import IndexView, GoodsListView, GoodsDetailView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),  # 主页
    url(r'^list/(?P<type_id>\d+)$', GoodsListView.as_view(), name='list'),  # 商品列表
    url(r'^detail/(?P<sku_id>\d+)$', GoodsDetailView.as_view(), name='detail')  # 商品详情

]
