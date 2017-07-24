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

last_code_re = re.compile(r'\D+(?P<code>\d+)$')
def getLastIntCode(str, default=0):
    if str is None:
        return default
    m = last_code_re.search(str)
    return int(m.group('code')) if m else default

pre_code_re = re.compile(r'^(?P<code>[a-zA-Z]+)\d+\w*$')
def getFirstCharCode(str, default=''):
    if str is None:
        return default
    m = pre_code_re.search(str)
    return m.group('code') if m else default

def call_delete_instance(code, model, all=False):
    if code:
        try:
            instance = model.objects.all().get(code=code)
            if instance and hasattr(instance, 'delete_instance'):
                instance.delete_instance(all=all)
        except model.DoesNotExist as e:
            pass

def get_instance(model, attr, value, create_no_exist=True, save_no_exist=False):
    instance = None
    try:
        instance = model.objects.all().get(**{attr: value})
    except model.DoesNotExist as e:
        pass
    if create_no_exist and instance is None:
        instance = model()
        setattr(instance, attr, value)
        if save_no_exist and instance:
            instance.save()
    return instance

def cmp(a, b):
    return a-b