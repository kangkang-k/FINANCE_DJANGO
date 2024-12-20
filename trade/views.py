from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Trade
from account.models import *
from budget.models import *
import json
from decimal import Decimal


@csrf_exempt
@login_required
def add_trade(request):
    if request.method == 'POST':
        try:
            # 获取请求中的 JSON 数据
            data = json.loads(request.body)

            # 获取各个字段
            account_id = data.get('account_id')
            budget_id = data.get('budget_id')
            traderemark = data.get('traderemark', '')
            tradebalance = data.get('tradebalance')
            tradetype = data.get('tradetype')

            # 验证字段是否缺失
            if not all([account_id, budget_id, tradebalance, tradetype]):
                return JsonResponse({
                    "code": 400,
                    "message": "缺少必要参数",
                    "data": {}
                })

            # 确保 tradebalance 是 Decimal 类型
            tradebalance = Decimal(str(tradebalance))  # 将 tradebalance 转为 Decimal 类型

            # 获取账户对象并确保是当前用户的账户
            try:
                account = Account.objects.get(id=account_id, user=request.user)
            except Account.DoesNotExist:
                return JsonResponse({
                    "code": 403,
                    "message": "不是当前用户的账户",
                    "data": {}
                })

            # 获取预算对象并确保是当前用户的预算
            try:
                budget = Budget.objects.get(id=budget_id, account__user=request.user)
            except Budget.DoesNotExist:
                return JsonResponse({
                    "code": 403,
                    "message": "不是当前用户的预算",
                    "data": {}
                })

            # 检查账户余额是否足够
            if tradetype in ['Dining', 'Transportation', 'Shopping', 'Entertainment', 'Education', 'Health', 'Housing',
                             'Communication', 'Personal Care', 'Insurance', 'Investments', 'Gifts']:
                if tradebalance > account.accountbalance:
                    return JsonResponse({
                        "code": 400,
                        "message": "账户余额不足",
                        "data": {}
                    })
                # 扣除余额
                account.accountbalance -= tradebalance
            else:
                # 增加余额（如充值等）
                account.accountbalance += tradebalance

            # 保存账户余额的更改
            account.save()

            # 创建交易记录
            trade = Trade.objects.create(
                account=account,
                budget=budget,
                traderemark=traderemark,
                tradebalance=tradebalance,
                tradetype=tradetype
            )

            return JsonResponse({
                "code": 200,
                "message": "交易记录添加成功",
                "data": {
                    "trade_id": trade.id,
                    "account_name": account.accountname,
                    "budget_name": budget.budgetname,
                    "tradebalance": trade.tradebalance,
                    "tradetype": trade.tradetype
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "code": 400,
                "message": "JSON 数据格式错误",
                "data": {}
            })
    else:
        return JsonResponse({
            "code": 405,
            "message": "仅支持 POST 请求",
            "data": {}
        })


@csrf_exempt
@login_required
def delete_trade(request):
    if request.method == 'POST':
        try:
            # 获取请求中的 JSON 数据
            data = json.loads(request.body)

            # 获取 trade_id 和 restore_balance 字段
            trade_id = data.get('trade_id')
            restore_balance = data.get('restore_balance', False)  # 默认不恢复余额

            if not trade_id:
                return JsonResponse({
                    "code": 400,
                    "message": "缺少交易记录 ID",
                    "data": {}
                })

            # 获取交易记录对象
            try:
                trade = Trade.objects.get(id=trade_id, account__user=request.user)
            except Trade.DoesNotExist:
                return JsonResponse({
                    "code": 404,
                    "message": "交易记录不存在或不是当前用户的记录",
                    "data": {}
                })

            # 获取账户对象
            account = trade.account

            # 如果需要恢复余额
            if restore_balance:
                if trade.tradetype in ['Dining', 'Transportation', 'Shopping', 'Entertainment', 'Education', 'Health',
                                       'Housing', 'Communication', 'Personal Care', 'Insurance', 'Investments',
                                       'Gifts']:
                    # 恢复账户余额：从账户中扣除该交易金额
                    account.accountbalance += trade.tradebalance
                elif trade.tradetype == 'Deposit':
                    # 如果是充值类型，增加账户余额
                    account.accountbalance -= trade.tradebalance
                else:
                    # 对于其他交易类型，如果有特定规则，也可以在此进行调整
                    pass

                # 更新账户余额
                account.save()

            # 删除交易记录
            trade.delete()

            return JsonResponse({
                "code": 200,
                "message": "交易记录删除成功",
                "data": {
                    "trade_id": trade_id,
                    "account_name": account.accountname,
                    "restore_balance": restore_balance
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "code": 400,
                "message": "JSON 数据格式错误",
                "data": {}
            })
    else:
        return JsonResponse({
            "code": 405,
            "message": "仅支持 POST 请求",
            "data": {}
        })


@csrf_exempt
@login_required
def get_trades(request):
    if request.method == 'GET':
        try:
            # 获取当前用户的所有交易记录
            trades = Trade.objects.filter(account__user=request.user)

            # 构造返回数据
            trade_data = []
            for trade in trades:
                trade_data.append({
                    "id": trade.id,
                    "account_name": trade.account.accountname,
                    "budget_name": trade.budget.budgetname if trade.budget else None,
                    "tradetype": trade.tradetype,
                    "tradebalance": str(trade.tradebalance),
                    "traderemark": trade.traderemark
                })

            return JsonResponse({
                "code": 200,
                "message": "交易记录查询成功",
                "data": trade_data
            })

        except Exception as e:
            return JsonResponse({
                "code": 500,
                "message": f"服务器错误: {str(e)}",
                "data": {}
            })
    else:
        return JsonResponse({
            "code": 405,
            "message": "仅支持 GET 请求",
            "data": {}
        })
