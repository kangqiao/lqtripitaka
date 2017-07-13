# -*- coding: UTF-8 -*-
__author__ = 'zhaopan'

from .models import Roll

class StrUtil(object):

    @classmethod
    def roll_type(code=""):
        '''
        根据code字符串去过滤出卷的类型
        :return: 返回卷的类型 @ref[Roll.TYPE_CHOICE]
        '''
        return Roll.TYPE_CHOICES[0][0]
