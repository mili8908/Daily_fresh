from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU
from apps.user.models import Address
from apps.order.models import OrderInfo, OrderGoods
from django.db import transaction
from django.http import JsonResponse
from datetime import datetime


class OrderPlaceView(LoginRequiredMixin, View):
    """提交订单页面"""
    def post(self, request):
        """显示"""
        # 获取登录用户
        user = request.user

        # 获取用户要购买商品的ids
        # request.POST->QueryDict类的对象，允许一个名字对应多个值
        # 去多个值的时候，需要调用对象的getlist方法
        sku_ids = request.POST.getlist('sku_ids')

        # 参数校验
        if not all(sku_ids):
            # 数据不完整，跳转到购物车页面

            return redirect(reverse('cart:show'))

        # 获取用户的收货地址信息
        addrs = Address.objects.filter(user=user)

        # 获取链接对象
        conn = get_redis_connection('default')

        # 拼接key
        cart_key = 'cart_%d'%user.id

        skus = []
        total_count = 0
        total_amount = 0
        # 获取用户所要购买的商品的信息
        for sku_id in sku_ids:
            # 根据商品的id查询商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)

            # 从redis中获取用户要购买的商品的数量
            # hget(key, field): 获取redis中sku_id属性的值
            count = conn.hget(cart_key, sku_id)

            # 计算购买商品的小计
            amount = sku.price*int(count)

            # 给sku对象增加属性count和amont
            # 分别保存用户要购买商品的数目和小计
            sku.count = int(count)
            sku.amount = amount

            # 追加商品
            skus.append(sku)

            # 累加计算用户要购买的商品的总件数和总金额
            total_count += int(count)
            total_amount += amount

        # 运费：10.0
        transit_price = 10

        # 实付款
        total_pay = total_amount + transit_price

        # 组织上下文
        sku_ids = ','.join(sku_ids)  # 1,4
        context = {'addrs': addrs,
                   'skus': skus,
                   'total_count': total_count,
                   'total_amount': total_amount,
                   'transit_price': transit_price,
                   'total_pay': total_pay,
                   'sku_ids': sku_ids}

        # 使用模板
        return render(request, 'place_order.html', context)


# 前端传递的参数: 收货地址id(addr_id) 支付方式(pay_method) 用户要购买的商品ids(sku_ids)(以,分隔字符串)
# 采用ajax post请求
# /order/commit
# 生成订单的流程:
    # 接收参数
    # 参数校验
    # 组织生成订单参数

    # todo: 向df_order_info表中添加一条记录

    # 遍历获取用户所要购买的商品的信息
        # 根据id查询商品的信息
        # 从redis中获取用户要购买的商品的数目
        # todo: 向df_order_goods表中添加一条记录

        # todo: 减少对应商品的库存，增加销量

        # todo: 累加计算用户要购买的商品的总数目和总金额

    # todo: 更新订单信息记录中的购买的商品的总数目和总金额

    # todo: 删除购物车中对应记录


class OrderCommitView(View):
    """订单创建"""
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})
        # 接收数据
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')
        # 验证数据
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '地址id不存在'})
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 3, 'errmsg': '数据非法'})
        # 组织生成订单参数
        # 订单id: 20180121120530 + 用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        transit_price = 10
        # 订单中商品的总数目和总金额
        total_count = 0
        total_price = 0
        order = OrderInfo.objects.create(order_id=order_id,
                                         user=user,
                                         addr=addr,
                                         pay_method=pay_method,
                                         total_count=total_count,
                                         total_price=total_price,
                                         transit_price=transit_price,
                                         )
        sku_ids = sku_ids.split(',')
        # 获取连接对象
        conn = get_redis_connection('default')
        # 拼接key
        cart_key = 'cart_%d' % user.id
        for sku_id in sku_ids:
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                return JsonResponse({'res': 4, 'errmsg': '商品不存在'})
            count = conn.hget(cart_key, sku_id)
            total_count += int(count)
            # 向df_order_goods表中添加一条记录
            OrderGoods.objects.create(order=order,
                                      sku=sku,
                                      count=int(count),
                                      price=sku.price)
            # 减少对应商品的库存，增加销量
            sku.stock -= int(count)
            sku.sales += int(count)
            sku.save()
            # 累加计算用户要购买的商品的总数目和总金额
            total_count += int(count)
            total_price += int(count)*sku.price
        # 更新订单信息记录中的购买的商品的总数目和总金额
        order.total_count = total_count
        order.total_price = total_price
        order.save()
        # 删除购物车中对应记录
        conn.hdel(cart_key, *sku_ids)
        # 返回应答
        return JsonResponse({'res': 5, 'message': '订单创建成功'})

















