from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views.generic import View
from .models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner, GoodsSKU
from django_redis import get_redis_connection
from apps.order.models import OrderGoods


class IndexView(View):
    """首页"""
    def get(self, request):
        """显示"""
        # 先尝试从缓存中获取数据
        context = cache.get('index_page_data')

        if context is None:
            print('设置首页缓存数据')
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
            # 组织模板上下文
            context = {'types': types,
                       'index_banner': index_banner,
                       'promotion_banner': promotion_banner,
                       'cart_count': cart_count}
            # 设置缓存: cache.set(缓存名称，缓存数据，缓存有效时间) pickle
            cache.set('index_page_data', context, 3600)

        # 获取登录用户购物车中商品的条目数
        # 获取user
        user = request.user
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')  # StrictRedis
            # 拼接key
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)

            context.update(cart_count=cart_count)
        # 使用模板
        return render(request, 'index.html', context)


class GoodsListView(View):
    def get(self, request, type_id):
        # 商品类名

        types = GoodsType.objects.all()
        # 获取type_id对应的分类信息type
        try:
            goods_type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            # 商品种类不存在，跳转到首页
            return redirect(reverse('goods:index'))
        skus = GoodsSKU.objects.filter(type=type_id)
        # 新品推荐(属于相同类型的商品)
        new_skus = GoodsSKU.objects.filter(type=type_id).order_by('-creat_time')[:2]

        # 组织上下文
        context = {
            'goods_type': goods_type,
            'types': types,
            'skus': skus,
            'new_skus': new_skus,
        }

        return render(request, 'list.html', context)


class GoodsDetailView(View):
    def get(self, request, sku_id):
        # 获取商品的分类信息
        types = GoodsType.objects.all()

        # 获取商品的详情信息
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在，跳转到首页
            return redirect(reverse('goods:index'))
        # 获取商品的评论信息
        # 获取商品的评论信息
        order_skus = OrderGoods.objects.filter(sku=sku).exclude(comment='').order_by('-update_time')

        # 获取和商品同一种类的2个新品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-creat_time')[:2]

        # 获取和商品同一个SPU其他规格商品
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=sku_id)

        # 获取登录用户购物车中商品的条目数
        cart_count = 0
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 查询redis数据库中的信息
            # 创建一个连接对象
            conn = get_redis_connection('default')
            # 拼接购物车信息条数的KEY
            cart_key = 'cart_%s' % user.id
            # 根据这个得到的key 查询Redis数据库
            cart_count = conn.hlen(cart_key)
            # 拼接历史记录的key
            history_key = 'history_%s' % user.id
            # 将这个内容添加到历史记录中
            # 如果用户浏览过该商品，先从redis对应list元素中先移除商品id
            # 在将商品id添加到列表的左侧
            # 拼接key
            history_key = 'history_%d' % user.id
            # lem：如果存在元素则移除，如果不存在什么都不做
            conn.lrem(history_key, 0, sku_id)
            # 将sku_id添加到列表的左侧
            conn.lpush(history_key, sku_id)
            # 保留列表的前5个商品的id
            conn.ltrim(history_key, 0, 4)

        # 组织上下文
        context = {
            'types': types,
            'sku': sku,
            'cart_count': cart_count,
            'order_skus': order_skus,
            'new_skus': new_skus,
            'same_spu_skus': same_spu_skus,
        }
        return render(request, 'detail.html', context)























