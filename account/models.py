from django.db import models
from django.conf import settings


class Account(models.Model):
    # 外键关联 User 表
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')

    # 账户名称
    accountname = models.CharField(max_length=255)

    # 账户类型，选择从 bank, wallet, ali, wechat
    ACCOUNT_TYPE_CHOICES = [
        ('bank', '银行'),
        ('wallet', '钱包'),
        ('ali', '支付宝'),
        ('wechat', '微信')
    ]
    accounttype = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)

    # 账户余额
    accountbalance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.accountname} ({self.accounttype})'
