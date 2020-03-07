from django.http import JsonResponse
from django.core.cache import cache

from common import keys
from user.logics import send_vcode
from user.models import User


def get_vcode(request):
    '''用户获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    result = send_vcode(phonenum)
    if result:
        return JsonResponse({'code': 0, 'data': None})
    else:
        return JsonResponse({'code': 1000, 'data': None})


def submit_vcode(request):
    '''用户提交验证码接口，并执行登陆注册'''
    # 获取参数
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    print(vcode)
    print(phonenum)
    cached_vcode = cache.get(keys.VCODE % phonenum)
    print(cached_vcode)

    # 检查验证码
    if vcode and cached_vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 将用户状态记录到Session
        request.session['uid'] = user.id

        return JsonResponse({'code': 0, 'data': user.to_dict()})

    else:
        return JsonResponse({'code': 1001, 'data': None})