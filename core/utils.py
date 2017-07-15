# -*- coding: UTF-8 -*-
__author__ = 'zhaopan'

import re
import operator


def roll_type(code=""):
    '''
    根据code字符串去过滤出卷的类型
    :return: 返回卷的类型 @ref[Roll.TYPE_CHOICE]
    '''
    #return Roll.TYPE_CHOICES[0][0]

def getLastInt(str, default=0):
    if str:
        return int(re.findall('\d+', str)[-1])
    else:
        return default

def cmp(a, b):
    return a-b