from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User
import re
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired


class RegisterView(View):
    """注册页面"""
    def get(self, request):

        return render(request, 'user/register.html')

    # web开发视图处理中通用的流程
    # 1 接收数据
    # 2 进行数据校验(后端校验)
    # 3 业务处理
    # 4 返回应答
    def post(self, request):
        # 1接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2进行数据校验
        # 校验数据完整性
        if not all([username, password, email]):
            return render(request, 'user/register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'user/register.html', {'errmsg': '邮箱格式不正确'})
        # 校验用户名是否存在
        try:
            user = User.objects.get(username=username)
        # get查询不到内容是捕获异常
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            return render(request, 'user/register.html', {'errmsg': '用户名已存在'})

        # 3业务处理
        user = User.objects.create_user(username, email, password)
        # 让用户名处于未激活状态
        user.is_active = 0
        user.save()
        # 注册成功之后需要给用户的注册邮箱发送激活邮件，在激活邮件中要包含激活链接
        # 激活链接: /user/active/用户id, 如果直接写用户id，其他人可能恶意请求网站
        # 解决方式: 先对用户身份信息加密，把加密后的信息放在激活链接中
        # /user/active/token信息

        # 使用itsdangerous生成激活的token信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        # 进行加密
        token = serializer.dump(info)  # bytes类型数据
        # 通过解码转换成str类型
        token = token.decode()
        send_register_active_email.delay(email, username, token)
        # 4返回应答  跳转回首页
        # return redirect('../goods/index')
        return redirect(reverse('user:login'))


#  /user/active/token信息
class ActiveView(View):
    """激活"""
    def get(self, request, token):
        """激活处理"""
        # 进行解密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']
            # 激活用户
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 返回应答 跳转到登录页面
            return redirect(reverse('goods:index'))
        except SignatureExpired as e:
            # 激活链接已失效
            # 实际开发：显示页面告诉用户激活链接已失效，让用户点击链接在发送一封激活邮件
            return HttpResponse('<h1>激活链接已失效</h1>')


# /user/login
class Login(View):
    """登录页面"""
    def get(self, request):
        # 尝试从cookie中获取用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get(username='username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'user/login.html', {'username': username, 'checked': checked})

    def post(self, request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 参数校验
        if not all([username, password]):
            return render(request, 'user/login.html', {'errmsg': '参数不完整'})
        # 业务处理：登录校验
        # 根据用户名和密码查找用户的信息
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # 账户已激活
                # 记住用户登录状态
                login(request, user)
                # 返回应答：跳转到首页
                # HttpResposeRedirect类->HttpResponse类的子类
                response = redirect(reverse('goods:index'))
                # 判断是否需要记住用户名
                remember = request.POST.get('checked')
                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    # 清除用户cookie
                    response.delete_cookie('username')
                return response

            else:
                # 账户未激活

                return render(request, 'user/login.html', {'errmsg': '账户未激活'})
        else:
            return render(request, 'user/login.html', {'errmsg': '用户名或密码错误'})


# /user/logout
class Logout(View):
    """退出登录"""
    def get(self, request):
        # 清除用户的登录状态
        logout(request)
        # 返回应答 跳转到登录
        return redirect(reverse('user:login'))



def user_info(request):
    """用户信息中心"""
    return render(request, 'user/user_center_info.html')


def user_order(request):
    """订单中心"""
    return render(request, 'user/user_center_order.html')


def user_site(request):
    """收货地址"""
    return render(request, 'user/user_center_site.html')