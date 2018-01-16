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


class AddressManager(models.Manager):
    """地址模型管理器类"""
    # 应用场景
    # 1.改变原有查询的结果集
    # 2.封装方法(操作模型类对应的数据表)
    def get_default_address(self, user):
        """获取用户的默认收货地址"""
        # self.model:获取self对象所在模型类
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # 用户不存在默认收货地址
            address = None

        # 返回address
        return address


class Address(BaseModel):
    """地址模型类"""

    user = models.ForeignKey('User', verbose_name='所属用户')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    addr = models.CharField(max_length=256, verbose_name='收货地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮编')
    phone = models.CharField(max_length=11, verbose_name='电话')
    id_default = models.BooleanField(default=False, verbose_name='是否默认')
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name










