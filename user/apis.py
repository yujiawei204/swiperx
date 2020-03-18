import os

from django.http import JsonResponse
from django.core.cache import cache

from common import keys
from common import stat
from user import logics
from user.models import User
from user.models import Profile
from user.forms import UserForm
from user.forms import ProfileForm


def get_vcode(request):
    '''用户获取验证码接口'''
    phonenum = request.GET.get('phonenum')
    result = logics.send_vcode(phonenum)
    if result:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.SMS_ERR, 'data': None})


def submit_vcode(request):
    '''用户提交验证码接口，并执行登陆注册'''
    # 获取参数
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    # print(vcode)
    # print(phonenum)

    cached_vcode = cache.get(keys.VCODE % phonenum)
    # print(cached_vcode)

    # 检查验证码
    if vcode and cached_vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 将用户状态记录到Session
        request.session['uid'] = user.id

        return JsonResponse({'code': stat.OK, 'data': user.to_dict()})

    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def get_profile(request):
    '''获取个人交友资料'''
    uid = request.session['uid']
    # try:
    #     profile = Profile.objects.get(id=uid)
    # except Profile.DoesNotExist:
    #     profile = Profile.objects.create(id=uid)
    profile, _ = Profile.objects.get_or_create(id=uid)
    return JsonResponse({'code':stat.OK, 'data':profile.to_dict()})


def set_profile(request):
    '''修改个人、交友资料'''

    # 验证用户表的数据
    user_form = UserForm(request.POST)
    if not user_form.is_valid():
        return JsonResponse({'code': stat.USER_FORM_ERR, 'data': user_form.errors})

    # 验证个人资料表的数据
    profile_form = ProfileForm(request.POST)
    if not profile_form.is_valid():
        return JsonResponse({'code': stat.PROFILE_FORM_ERR, 'data': profile_form.errors})

    # 更新user数据
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    user.__dict__.update(user_form.cleaned_data)

    # 更新Profile数据
    profile, _ = Profile.objects.get_or_create(id=uid)
    profile.__dict__.update(profile_form.cleaned_data)

    user.save()
    profile.save()
    return JsonResponse({'code': stat.OK, 'data': None})


def upload_avatar(request):
    '''上传个人头像接口'''

    # 取出文件对象
    uid = request.session.get('uid')
    avatar_file = request.FILES.get('avatar')

    logics.upload_avatar_celery.delay(uid, avatar_file)

    return JsonResponse({'code': stat.OK, 'data': None})





















