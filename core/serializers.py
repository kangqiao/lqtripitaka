# -*- coding: UTF-8 -*-

__author__ = 'zhaopan'

from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TranslatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Translator
        fields = '__all__'
