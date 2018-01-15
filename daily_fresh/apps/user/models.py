from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser


# 使用django默认的认证系统
# python manage.py createsuperuser->auth_user->User模型类
class User(AbstractUser, BaseModel):
    """用户模型类"""

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        # 去掉结尾的s
        verbose_name_plural = verbose_name


class Address(BaseModel):
    """地址模型类"""

    user = models.ForeignKey('User', verbose_name='所属用户')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    addr = models.CharField(max_length=256, verbose_name='收货地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮编')
    phone = models.CharField(max_length=11, verbose_name='电话')
    id_default = models.BooleanField(default=False, verbose_name='是否默认')

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name










