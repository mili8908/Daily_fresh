from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField


class GoodsType(BaseModel):
    """商品类型模型类"""

    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='雪碧图')
    image = models.ImageField(upload_to=type, verbose_name='商品类型图片')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):
    """商品SKU模型类"""

    status_choices = (
        (0, '下架'),
        (1, '上架')
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品种类')
    goods = models.ForeignKey('Goods', verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    stock = models.IntegerField(default=1, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='状态')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    """商品SPU模型类"""
    name = models.CharField(max_length=20, verbose_name='商品spu名称')
    # 不是Django应用 来自tinymce  富文本编辑框
    detail = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    """商品图片模型类"""

    sku = models.ForeignKey('GoodsSKU', verbose_name='商品')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    """首页轮播图片模型类"""

    sku = models.ForeignKey('GoodsSKU', verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='banner图')
    index = models.SmallIntegerField(default=0, verbose_name='轮播顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '主页banner图'
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):
    """首页分类图片模型类"""

    display_type_choices = {
        (0, '标题'),
        (1, '图片')
    }
    type = models.ForeignKey('GoodsType', verbose_name='商品类型')  # 种类外键
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品')  # sku外键
    display_type = models.SmallIntegerField(default=1, choices=display_type_choices, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = '首页分类图片展示'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    """首页促销活动图片模型类"""

    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.CharField(max_length=256, verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name













