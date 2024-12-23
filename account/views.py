from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Account
import json


@login_required
@csrf_exempt
def add_account(request):
    if request.method == 'POST':
        try:
            # 解析请求中的 JSON 数据
            data = json.loads(request.body)
            accountname = data.get('accountname')
            accounttype = data.get('accounttype')

            # 验证账户类型是否有效
            if accounttype not in dict(Account.ACCOUNT_TYPE_CHOICES).keys():
                return JsonResponse({
                    "code": 400,
                    "message": "无效的账户类型",
                    "data": {}
                })

            # 创建账户记录，设置默认余额为 0
            account = Account.objects.create(
                user=request.user,
                accountname=accountname,
                accounttype=accounttype,
                accountbalance=0.00  # 设置默认余额为 0
            )

            # 返回创建成功的账户信息
            return JsonResponse({
                "code": 200,
                "message": "账户创建成功",
                "data": {
                    "accountname": account.accountname,
                    "accounttype": account.accounttype,
                    "accountbalance": str(account.accountbalance)  # 返回字符串以便 JSON 序列化
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
def delete_account(request):
    if request.method == 'POST':
        try:
            account_id = json.loads(request.body).get('account_id')
            # 查找账户
            account = Account.objects.get(id=account_id, user=request.user)

            # 删除账户
            account.delete()

            return JsonResponse({
                "code": 200,
                "message": "账户删除成功",
                "data": {}
            })

        except Account.DoesNotExist:
            return JsonResponse({
                "code": 404,
                "message": "账户不存在或不属于当前用户",
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
def get_user_accounts(request):
    # 获取当前登录用户的所有账户
    accounts = Account.objects.filter(user=request.user)

    # 如果没有账户，返回提示信息
    if not accounts.exists():
        return JsonResponse({
            "code": 404,
            "message": "当前用户没有账户",
            "data": {}
        })

    # 构建账户信息列表
    account_data = [
        {
            "accountid": account.id,
            "accountname": account.accountname,
            "accounttype": account.accounttype,
            "accountbalance": str(account.accountbalance)
        }
        for account in accounts
    ]

    return JsonResponse({
        "code": 200,
        "message": "获取用户账户信息成功",
        "data": account_data
    })


@login_required
@csrf_exempt
def update_account(request):
    if request.method == 'POST':
        try:
            # 获取请求中的 JSON 数据
            data = json.loads(request.body)
            account_id = data.get('account_id')
            accountname = data.get('accountname')
            accounttype = data.get('accounttype')

            # 查找账户，确保账户属于当前登录用户
            account = Account.objects.get(id=account_id, user=request.user)

            # 更新账户信息
            if accountname:
                account.accountname = accountname
            if accounttype:
                # 验证账户类型是否有效
                if accounttype not in dict(Account.ACCOUNT_TYPE_CHOICES).keys():
                    return JsonResponse({
                        "code": 400,
                        "message": "无效的账户类型",
                        "data": {}
                    })
                account.accounttype = accounttype

            # 保存修改
            account.save()

            return JsonResponse({
                "code": 200,
                "message": "账户信息更新成功",
                "data": {
                    "accountname": account.accountname,
                    "accounttype": account.accounttype,
                    "accountbalance": str(account.accountbalance)  # 保持余额原样返回
                }
            })

        except Account.DoesNotExist:
            return JsonResponse({
                "code": 404,
                "message": "账户不存在或不属于当前用户",
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
def get_account_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            account_id = data.get('account_id')
            account = Account.objects.get(id=account_id, user=request.user)
            return JsonResponse({
                "code": 200,
                "message": "账户信息获取成功",
                "data": {
                    "accountname": account.accountname,
                    "accounttype": account.accounttype,
                    "accountbalance": str(account.accountbalance)
                }
            })
        except Account.DoesNotExist:
            return JsonResponse({
                "code": 404,
                "message": "账户不存在或不属于当前用户",
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
