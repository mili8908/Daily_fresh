from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU
from apps.user.models import Address


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


# class OrderCommitView(View):
#     """订单创建"""
#     def post(self, request):