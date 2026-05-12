from django.db import models

# Create your models here.
class User(models.Model):
    """用户表"""
    username = models.CharField('用户名',max_length = 100,unique=True)
    password = models.CharField('密码',max_length = 128)
    email = models.CharField('邮箱',max_length = 50,unique=True)
    user_text = models.TextField(blank=True, null=True,verbose_name='个人简介')

    class Meta:
        # 表名
        db_table = 'users'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class Data(models.Model):
    """淘宝数据集"""
    title = models.CharField(max_length=500, null=True, blank=True, verbose_name='商品标题')
    shop = models.CharField(max_length=100, null=True, blank=True, verbose_name='店铺名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='商品价格')
    pay_count = models.IntegerField(null=True, blank=True, verbose_name='付款人数')
    ship_address = models.CharField(max_length=100, null=True, blank=True, verbose_name='发货地址')
    detail_url = models.TextField(null=True, blank=True, verbose_name='详情页地址')
    image_url = models.TextField(null=True, blank=True, verbose_name='图片地址')
    features = models.TextField(null=True, blank=True, verbose_name='特点列表')
    selling_points = models.TextField(null=True, blank=True, verbose_name='卖点')
    product_brand = models.CharField(max_length=100, null=True, blank=True, verbose_name='商品品牌')

    class Meta:
        db_table = 'data'
        verbose_name = '淘宝商品数据'
        verbose_name_plural = '淘宝商品数据'
        ordering = ['-id']

    def __str__(self):
        return self.title if self.title else f"商品ID:{self.id}"


class LoginStatistics(models.Model):
    """登录统计表"""
    date = models.DateField(verbose_name='统计日期')
    login_count = models.IntegerField(default=0, verbose_name='登录数量')

    class Meta:
        db_table = 'login_statistics'
        verbose_name = '登录统计'
        verbose_name_plural = '登录统计'

    def __str__(self):
        return f"{self.date} - {self.login_count}次登录"