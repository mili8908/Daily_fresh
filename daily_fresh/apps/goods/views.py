from django.shortcuts import render
from django.views.generic import View
from .models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from django_redis import get_redis_connection


class IndexView(View):
    """首页"""
    def get(self, request):
        """显示"""
        # 获取商品分类信息
        types = GoodsType.objects.all()
        # 获取首页轮播商品信息
        index_banner = IndexGoodsBanner.objects.all().order_by('index')
        # 获取促销活动商品信息
        promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

        # 获取首页分类商品展示的信息
        for type in types:
            # 查询type种类首页展示的文字商品的信息
            title_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
            # 查询type种类首页展示的图片商品的信息
            image_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')

            # 给type对象增加属性title_banner和image_banner
            # 分别保存type中类首页展示的文字商品信息和图片商品的信息
            type.title_banner = title_banner
            type.image_banner = image_banner

        # 获取登录用户购物车中商品的条目数
        cart_count = 0
        # 获取user
        user = request.user
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')  # StrictRedis
            # 拼接key
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context = {'types': types,
                   'index_banner': index_banner,
                   'promotion_banner': promotion_banner,
                   'cart_count': cart_count}

        # 使用模板
        return render(request, 'index.html', context)


class GoodsListView(View):
    def get(self, request):

        return render(request, 'list.html')


class GoodsDetailView(View):
    def get(self, request):

        return render(request, 'detail.html')