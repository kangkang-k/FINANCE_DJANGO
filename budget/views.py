from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Budget
from account.models import Account
import json


@login_required
@csrf_exempt
def add_budget(request):
    if request.method == 'POST':
        try:
            # 获取请求中的 JSON 数据
            data = json.loads(request.body)
            account_id = data.get('account_id')
            budgetname = data.get('budgetname')
            budgettype = data.get('budgettype')
            budgetbalance = data.get('budgetbalance')

            try:
                account = Account.objects.get(id=account_id, user=request.user)
            except Account.DoesNotExist:
                return JsonResponse({
                    "code": 404,
                    "message": "账户不存在或不属于当前用户",
                    "data": {}
                })

            # 验证预算类型是否合法
            if budgettype not in dict(Budget.BUDGET_TYPE_CHOICES).keys():
                return JsonResponse({
                    "code": 400,
                    "message": "无效的预算类型",
                    "data": {}
                })

            # 验证预算余额是否为有效数字
            try:
                budgetbalance = float(budgetbalance)
            except ValueError:
                return JsonResponse({
                    "code": 400,
                    "message": "无效的预算余额",
                    "data": {}
                })

            # 创建新的预算对象并保存
            budget = Budget.objects.create(
                account=account,
                budgetname=budgetname,
                budgettype=budgettype,
                budgetbalance=budgetbalance
            )

            return JsonResponse({
                "code": 200,
                "message": "预算添加成功",
                "data": {
                    "budgetname": budget.budgetname,
                    "budgettype": budget.budgettype,
                    "budgetbalance": str(budget.budgetbalance)
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


@login_required
@csrf_exempt
def delete_budget(request):
    if request.method == 'POST':
        try:
            # 获取请求中的 JSON 数据
            data = json.loads(request.body)
            budget_id = data.get('budget_id')

            # 查询预算，确保是当前用户的预算
            try:
                budget = Budget.objects.get(id=budget_id)
            except Budget.DoesNotExist:
                return JsonResponse({
                    "code": 404,
                    "message": "预算未找到",
                    "data": {}
                })

            # 检查预算是否属于当前用户
            if budget.account.user != request.user:
                return JsonResponse({
                    "code": 403,
                    "message": "此预算不是当前用户的预算",
                    "data": {}
                })

            # 删除预算
            budget.delete()

            return JsonResponse({
                "code": 200,
                "message": "预算删除成功",
                "data": {}
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


@login_required
@csrf_exempt
def update_budget(request):
    if request.method == 'POST':
        try:
            # 获取请求中的 JSON 数据
            data = json.loads(request.body)
            budget_id = data.get('budget_id')
            budgetname = data.get('budgetname')
            budgettype = data.get('budgettype')
            budgetbalance = data.get('budgetbalance')

            # 查询预算，确保是当前用户的预算
            try:
                budget = Budget.objects.get(id=budget_id)
            except Budget.DoesNotExist:
                return JsonResponse({
                    "code": 404,
                    "message": "预算未找到",
                    "data": {}
                })

            # 检查预算是否属于当前用户
            if budget.account.user != request.user:
                return JsonResponse({
                    "code": 403,
                    "message": "此预算不是当前用户的预算",
                    "data": {}
                })

            # 更新预算信息
            if budgetname:
                budget.budgetname = budgetname
            if budgettype:
                budget.budgettype = budgettype
            if budgetbalance is not None:
                budget.budgetbalance = budgetbalance

            # 保存更新后的预算
            budget.save()

            return JsonResponse({
                "code": 200,
                "message": "预算修改成功",
                "data": {
                    "budget_id": budget.id,
                    "budgetname": budget.budgetname,
                    "budgettype": budget.budgettype,
                    "budgetbalance": budget.budgetbalance
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


@login_required
@csrf_exempt
def get_user_budgets(request):
    budgets = Budget.objects.filter(account__user=request.user)
    if not budgets.exists():
        return JsonResponse({
            "code": 404,
            "message": "当前用户没有预算",
            "data": {}
        })
    budget_list = []
    for budget in budgets:
        budget_list.append({
            "budgetid": budget.id,
            "budgetname": budget.budgetname,
            "budgettype": budget.budgettype,
            "budgetbalance": str(budget.budgetbalance),
            "accountname": budget.account.accountname,
            "accounttype": budget.account.accounttype,
        })

    return JsonResponse({
        "code": 200,
        "message": "获取用户预算记录成功",
        "data": budget_list
    })


@login_required
@csrf_exempt
def get_budget_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            budget_id = data.get('budget_id')
            accounts = Account.objects.filter(user=request.user)
            if not accounts:
                return JsonResponse({
                    "code": 404,
                    "message": "用户没有账户",
                    "data": {}
                })

            # 获取预算的 account_id 参数
            account_id = data.get('account_id')
            # 确保传入的 account_id 属于当前用户
            account = accounts.get(id=account_id)
            if not account:
                return JsonResponse({
                    "code": 404,
                    "message": "账户不存在或不属于当前用户",
                    "data": {}
                })

            # 获取与 account 相关联的预算
            budget = Budget.objects.get(id=budget_id, account=account)

            return JsonResponse({
                "code": 200,
                "message": "预算信息获取成功",
                "data": {
                    "budgetname": budget.budgetname,
                    "budgettype": budget.budgettype,
                    "budgetbalance": str(budget.budgetbalance)
                }
            })
        except Budget.DoesNotExist:
            return JsonResponse({
                "code": 404,
                "message": "预算不存在或不属于当前账户",
                "data": {}
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


