from django.shortcuts import render
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU
from django.http import JsonResponse


class CartInfoView(LoginRequiredMixin, View):
    """显示购物车页面"""
    def get(self, request):
        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # 从redis中获取用户购物车记录
        # hgetall(key): 返回值是一个字典，字典键就是属性，键对应的值就是属性的值
        cart_dict = conn.hgetall(cart_key)  # {'sku_id':商品数量}
        skus = []
        # 商品总数
        total_count = 0
        # 总价
        total_amount = 0

        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            sku.count = count
            total_count += int(count)
            # 小计
            sku.price = sku.price
            amount = sku.price*int(count)
            sku.amount = amount
            total_amount += amount

            skus.append(sku)

        context = {
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
        }

        return render(request, 'cart.html', context)


# 前端需要传递的参数：商品id(sku_id) 商品数量(count)
# 采用ajax post请求
# /cart/add
class CartAddView(View):
    """购物车记录添加"""
    def post(self, request):
        user = request.user
        # 验证用户是否登录
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})
        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 验证数据完整性
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})
        try:
            count = int(count)
        except:
            return JsonResponse({'res': 3, 'errmsg': '数据格式非法'})
        if count <= 0:
            return JsonResponse({'res': 3, 'errmsg': '商品数目非法'})

        # 建立连接
        conn = get_redis_connection('default')
        # 拼接key
        cart_key = 'cart_%d' % user.id
        # 如果用户的购物车中已经添加过该商品，则商品的数目需要累加
        # hget(key, field): 如果存在field返回是对应值，如果不存在field，返回None
        cart_count = conn.hget(cart_key, sku.id)

        if cart_count:
            count += int(cart_count)
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '数量超出库存'})

        conn.hset(cart_key, sku_id, count)

        # 获取用户购物车中商品的条目数
        cart_count = conn.hlen(cart_key)

        # 返回应答
        return JsonResponse({'res': 5, 'cart_count': cart_count, 'message': "添加成功"})


# 前端需要传递的参数：商品id(sku_id) 更新数量(count)
# 采用ajax post请求
# /cart/update
class CartUpdateView(View):
    """购物车记录-更新"""
    def post(self, request):
        """更新"""
        # 获取登录用户
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 参数校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验商品id
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 校验商品的数量count
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 3, 'errmsg': '商品数目非法'})

        if count <= 0:
            return JsonResponse({'res': 3, 'errmsg': '商品数目非法'})

        # 业务处理：更新用户购物车记录信息
        # 获取链接
        conn = get_redis_connection('default')

        # 拼接key
        cart_key = 'cart_%d' % user.id

        # 判断商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
        # 更新用户购物车中商品的数目
        # hset(cart_key, field, val)
        conn.hset(cart_key, sku_id, count)

        # 计算用户购物车中商品的总件数
        # hvals(key): 返回所有属性的值，返回的是一个列表
        cart_vals = conn.hvals(cart_key)
        cart_count = 0

        for val in cart_vals:
            cart_count += int(val)

        # 返回应答
        return JsonResponse({'res': 5, 'cart_count': cart_count, 'message': '更新成功'})


class CartDeleteView(View):
    """删除商品"""
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})
        # 获得参数
        sku_id = request.POST.get('sku_id')
        if not all(sku_id):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 建立连接
        conn = get_redis_connection('default')
        # 拼接Key
        cart_key = 'cart_%d' % user.id
        # 删除
        conn.hdel(cart_key, sku_id)
        # 计算用户购物车中商品的总件数
        # hvals(key): 返回所有属性的值，返回的是一个列表
        cart_vals = conn.hvals(cart_key)
        cart_count = 0
        for val in cart_vals:
            cart_count += int(val)

        # 返回应答
        return JsonResponse({'res': 3, 'cart_count': cart_count, 'message': '删除成功'})