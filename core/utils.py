# -*- coding: UTF-8 -*-
__author__ = 'zhaopan'

import re

ROLL_TYPE_CHOICES = (
    ('roll', '卷'),
    ('preface', '序'),
    ('all_preface', '总序'),
    ('origin_preface', '原序'),
    ('catalogue', '总目'),
    ('postscript', '跋'),
    ('corrigenda', "勘误表")
)
origin_roll_type_dict = dict(ROLL_TYPE_CHOICES)
preface_re = re.compile(r'(?P<type>' +'|'.join(origin_roll_type_dict.values()) + ')', re.M)
roll_type_dict = dict([(v,k) for k,v in origin_roll_type_dict.items()])
def get_roll_type(str, default='preface'):
    if not str:
        return default
    m = preface_re.search(str)
    val = m.group('type') if m else '序'
    return roll_type_dict.get(val, default)

def get_roll_type_desc(type, default='序'):
    return origin_roll_type_dict.get(type, default)

roll_type_re = re.compile(r'\w+_(?P<type>[a-zA-Z]+)')
def extract_roll_type(code, default='preface'):
    if not str:
        return default
    m = roll_type_re.search(code)
    return m.group('type') if m else default


SUTRA_TYPE_CHOICES = (
    ('ST', '经'), # SUTTA
    ('RT', '律'), # RESTRAIN
    ('TT', '论'), # TREATISE
)
origin_sutra_type_dict = dict(SUTRA_TYPE_CHOICES)
sutra_re = re.compile(r'(?P<type>' +'|'.join(origin_sutra_type_dict.values()) + ')', re.M)
sutra_type_dict = dict([(v,k) for k,v in origin_sutra_type_dict.items()])
def get_sutra_type(str, default='ST'):
    if not str:
        return default
    m = sutra_re.search(str)
    val = m.group('type') if m else '经'
    return sutra_type_dict.get(val, default)

def get_sutra_type_desc(type, default='经'):
    return origin_sutra_type_dict.get(type, default)


last_code_re = re.compile(r'\D+(?P<code>\d+)$')
def getLastIntCode(str, default=0):
    if not str:
        return default
    m = last_code_re.search(str)
    return int(m.group('code')) if m else default

pre_code_re = re.compile(r'^(?P<code>[a-zA-Z]+)\d+\w*$')
def getFirstCharCode(codestr, default=''):
    if not codestr:
        return default
    m = pre_code_re.search(str(codestr))
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