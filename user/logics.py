import random

import requests
from django.core.cache import cache

from swiper import cfg
from common import keys


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
    print(args['mobile'])
    if response.status_code != 200:
        return False
    else:
        cache.set(keys.VCODE % phonenum, vcode, 180)
        return True
