from django.shortcuts import render, redirect
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU


class OrderPlaceView(LoginRequiredMixin, View):
    """提交订单页面"""
    def post(self, request):

        return render(request, 'place_order.html')

    def get(self, request):
        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_dict = conn.hgetall(cart_key)
        skus = []
        total_count = 0
        total_amount = 0

        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            sku.count = count
            total_count += int(count)
            amount = sku.price * int(count)
            sku.amount = amount
            total_amount += amount
            skus.append(sku)
        transit_price = 10
        finally_price = total_amount + transit_price

        context = {
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'transit_price': transit_price,
            'finally_price': finally_price,
        }

        return render(request, 'place_order.html', context)
