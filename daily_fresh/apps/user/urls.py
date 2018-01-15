from django.conf.urls import url
from apps.user.views import Login, RegisterView, ActiveView


urlpatterns = [
    url(r'^login$', Login.as_view(), name='login'),  # 登录页面
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册页面
    url(r'^active/(?P<token>.*)', ActiveView.as_view(), name='active'),  # 激活
    # url(r'^user_center_info$', views.user_info, name='user_center_info'),  # 信息中心
    # url(r'^user_center_order$', views.user_order, name='user_center_order'),  # 订单中心
    # url(r'^user_center_site$', views.user_site, name='user_center_site'),  # 地址信息
]
