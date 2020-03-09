from django.db import models


# Create your models here.

class User(models.Model):
    '''用户表'''
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
    avatar = models.CharField(max_length=256, verbose_name='头像')
    location = models.CharField(max_length=16, choices=LOCATION, default='北京', verbose_name='居住地')

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }


class Profile(models.Model):
    '''用户交友资料表 '''
    dating_sex = models.CharField(max_length=8, choices=User.SEX, verbose_name='匹配的性别')
    location = models.CharField(max_length=16, choices=User.LOCATION, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最⼩查找范围')
    max_distance = models.IntegerField(default=30, verbose_name='最⼤查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最⼩交友年年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年年龄')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的⼈人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    def to_dict(self):
        return {
            'id': self.id,
            'dating_sex': self.dating_sex,
            'location': self.location,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matche': self.only_matche,
            'auto_play': self.auto_play
        }







