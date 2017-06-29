# -*- coding: UTF-8 -*-

__author__ = 'zhaopan'

from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class TranslatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Translator
        fields = '__all__'


class PageResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageResource
        fields = ('type', 'resource')


class PageSerializer(serializers.ModelSerializer):
    page_resources = PageResourceSerializer(many=True)

    class Meta:
        model = Page
        fields = '__all__'


class RollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roll
        fields = '__all__'


class SutraSerializer(serializers.ModelSerializer):
    rolls = RollSerializer(many=True)

    class Meta:
        model = Sutra
        fields = '__all__'


class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        fields = '__all__'


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    volumes = VolumeSerializer(many=True)
    sutras = SutraSerializer(many=True)

    def to_representation(self, instance):
        '''
            to_representation 将从 Model 取出的数据 parse 给 Api
            to_internal_value 将客户端传来的 json 数据 parse 给 Model
            当请求版本列表时, 不显示版本的目录信息.
            参考: https://github.com/dbrgn/drf-dynamic-fields/blob/master/drf_dynamic_fields/__init__.py
        '''
        request = self.context['request']
        if request.resolver_match.url_name == 'series-list':
            self.fields.pop("volumes", None)
            self.fields.pop("sutras", None)
        return super().to_representation(instance)

    class Meta:
        model = Series
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
