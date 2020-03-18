import os
import random

import requests
from django.core.cache import cache

from swiper import cfg
from common import keys
from user.models import User
from libs.qn_cloud import upload_to_qn
from tasks import celery_app


def gen_rand_code(length=6):
    '''产生出指定长度的随机码'''
    codes = []
    for i in range(length):
        num = random.randint(0, 9)
        codes.append(str(num))
    return ''.join(codes)


def send_vcode(phonenum):
    '''发送验证码'''
    vcode = gen_rand_code()
    print('验证码：%s' % vcode)
    args = cfg.YZX_SMS_ARGS.copy()
    args['param'] = vcode
    args['mobile'] = phonenum
    response = requests.post(cfg.YZX_SMS_API, json=args)
    # print(args['mobile'])

    if response.status_code != 200:
        return False
    else:
        cache.set(keys.VCODE % phonenum, vcode, 180)
        # print(keys.VCODE % phonenum)

        return True


def save_upload_avatar(uid, upload_avatar_file):
    filename = 'Avatar-%s' % uid
    filepath = '/tmp/%s' % filename

    with open(filepath, 'wb') as fp:
        for chunk in upload_avatar_file.chunks():
            fp.write(chunk)

    return filename, filepath


@celery_app.task
def upload_avatar_celery(uid, avatar_file):
    '''上传头像的过程'''
    # 将文件对象保存到本地
    filename, filepath = save_upload_avatar(uid, avatar_file)

    # 将文件上传到文件云
    avatar_url = upload_to_qn(filename, filepath)

    # 保存文件的URL
    user = User.objects.get(id=uid)
    user.avatar = avatar_url
    user.save()

    # 删除本地文件
    os.remove(filepath)