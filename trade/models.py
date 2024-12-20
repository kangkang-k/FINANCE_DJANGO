from django.db import models
from django.conf import settings


class Trade(models.Model):
    # 外键关联账户表（account app中的 Account 模型）
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='trades')

    # 外键关联预算表（budget app中的 Budget 模型）
    budget = models.ForeignKey('budget.Budget', on_delete=models.CASCADE, related_name='trades')

    # 交易备注
    traderemark = models.CharField(max_length=255, blank=True, null=True)

    # 交易金额
    tradebalance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # 交易类型，选择项
    TRADE_TYPE_CHOICES = [
        ('Dining', '餐饮'),
        ('Transportation', '交通'),
        ('Shopping', '购物'),
        ('Entertainment', '娱乐'),
        ('Education', '教育'),
        ('Health', '健康'),
        ('Housing', '住房'),
        ('Communication', '通讯'),
        ('Personal Care', '个人护理'),
        ('Insurance', '保险'),
        ('Investments', '投资'),
        ('Gifts', '礼物')
    ]
    tradetype = models.CharField(max_length=50, choices=TRADE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.tradetype} - {self.tradebalance} - {self.account.accountname}"

