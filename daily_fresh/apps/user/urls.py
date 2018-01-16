from django.conf.urls import url
from apps.user.views import Login, RegisterView, ActiveView, Logout, UserInfo, UserOrder, UserSite


urlpatterns = [
    url(r'^login$', Login.as_view(), name='login'),  # 登录页面
    url(r'^logout$', Logout.as_view(), name='logout'),  # 登录页面
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册页面
    url(r'^active/(?P<token>.*)', ActiveView.as_view(), name='active'),  # 激活
    url(r'^user_center_info$', UserInfo.as_view(), name='user_center_info'),  # 信息中心
    url(r'^user_center_order$', UserOrder.as_view(), name='user_center_order'),  # 订单中心
    url(r'^user_center_site$', UserSite.as_view(), name='user_center_site'),  # 地址信息
]
