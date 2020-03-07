from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性')
    )
    LOCATION = (
        ('上海', '上海'),
        ('北京', '北京'),
        ('广东', '广东'),
        ('南京', '南京'),
        ('重庆', '重庆'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('长沙', '长沙')
    )
    phonenum = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, default='male', verbose_name='性别')
    birthday = models.DateField(default='1990-1-1', verbose_name='生日')
    avatar = models.ImageField(max_length=256, verbose_name='头像')
    location = models.CharField(max_length=16, choices=LOCATION, default='北京', verbose_name='居住地')