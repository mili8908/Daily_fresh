from django.contrib import admin
from django.core.cache import cache
from .models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
# from celery_tasks.tasks import generate_static_index_html


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # 先继承
        super().save_model(request, obj, form, change)
        print('发出generate_static_index_html任务')
        # 重新生成一个静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        # 附加操作: 清除首页缓存数据
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        print('发出generate_static_index_html任务')
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        cache.delete('index_page_data')


class GoodsTypeAdmin(BaseAdmin):
    pass


class IndexGoodsBannerAdmin(BaseAdmin):
    pass


class IndexPromotionBannerAdmin(BaseAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseAdmin):
    pass


admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
