from django.http import JsonResponse

from user.logics import send_vcode


def get_vcode(request):
    '''用户获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    result = send_vcode(phonenum)
    if result:
        return JsonResponse({'code': 0, 'data': None})
    else:
        return JsonResponse({'code': 1000, 'data': None})


def submit_vcode(request):
    '''用户提交验证码接口'''

    pass
