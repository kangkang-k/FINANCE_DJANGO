from django.db import models

class Budget(models.Model):
    # 外键关联 Account 表，确保引用正确的 app 和模型
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='budgets')

    # 预算名称
    budgetname = models.CharField(max_length=255)

    # 预算类型，选择项包括：Dining、Transportation、Shopping、Entertainment、Education、Health、Housing、Communication、Personal Care、Insurance、Investments、Gifts
    BUDGET_TYPE_CHOICES = [
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
        ('Gifts', '礼物'),
    ]
    budgettype = models.CharField(max_length=20, choices=BUDGET_TYPE_CHOICES)

    # 预算余额
    budgetbalance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.budgetname} ({self.get_budgettype_display()})'

