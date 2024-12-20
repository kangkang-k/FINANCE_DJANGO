import json

from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout
from django.contrib.auth.decorators import login_required

User = get_user_model()


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "code": 409,
                    "message": "用户名已存在",
                    "data": {}
                })

            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "code": 409,
                    "message": "邮箱已被注册",
                    "data": {}
                })

            user = User.objects.create_user(username=username, email=email, password=password)

            return JsonResponse({
                "code": 200,
                "message": "注册成功",
                "data": {"username": user.username, "email": user.email}
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
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # 查找用户
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({
                    "code": 401,
                    "message": "用户不存在",
                    "data": {}
                })

            # 检查密码是否正确
            if not user.check_password(password):
                return JsonResponse({
                    "code": 401,
                    "message": "密码错误",
                    "data": {}
                })

            # 检查用户是否被禁用
            if not user.is_active:
                return JsonResponse({
                    "code": 403,
                    "message": "资金异常，账号已冻结，请联系管理员",
                    "data": {}
                })
            auth_login(request,user)
            # 登录成功
            return JsonResponse({
                "code": 200,
                "message": "登录成功",
                "data": {
                    "username": user.username,
                    "email": user.email
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
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nickname = data.get('nickname')
            birthday = data.get('birthday')
            gender = data.get('gender')
            email = data.get('email')

            user = request.user

            if nickname:
                user.nickname = nickname
            if birthday:
                user.birthday = birthday
            if gender:
                if gender not in ['M', 'F', 'O']:
                    return JsonResponse({
                        "code": 400,
                        "message": "性别参数无效",
                        "data": {}
                    })
                user.gender = gender
            if email:
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    return JsonResponse({
                        "code": 409,
                        "message": "该邮箱已被占用",
                        "data": {}
                    })
                user.email = email

            user.save()

            return JsonResponse({
                "code": 200,
                "message": "个人信息更新成功",
                "data": {
                    "username": user.username,
                    "nickname": user.nickname,
                    "birthday": user.birthday,
                    "gender": user.gender,
                    "email": user.email
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
def get_user_info(request):
    # 检查是否有用户登录
    if not request.user.is_authenticated:
        return JsonResponse({
            "code": 401,
            "message": "无用户登录",
            "data": {}
        })

    user = request.user
    user_info = {
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "birthday": user.birthday,
        "gender": user.gender
    }

    return JsonResponse({
        "code": 200,
        "message": "获取用户信息成功",
        "data": user_info
    })


@login_required
@csrf_exempt
def logout_user(request):
    # 调用 Django 自带的 logout 函数，退出当前用户
    logout(request)

    return JsonResponse({
        "code": 200,
        "message": "退出登录成功",
        "data": {}
    })
