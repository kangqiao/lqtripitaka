# -*- coding: UTF-8 -*-

__author__ = 'zhaopan'

from .settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lqtripitaka',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'lqtripitaka',
    #     'USER': 'dzj',
    #     'PASSWORD': 'dzjsql',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    #     'CONN_MAX_AGE': 600,
    # }
}
