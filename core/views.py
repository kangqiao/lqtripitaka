from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *


class SeriesSet(viewsets.ReadOnlyModelViewSet):
    """
        查看 版本API
    """
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class VolumeSet(viewsets.ReadOnlyModelViewSet):
    """
        查看 册API
    """
    queryset = Volume.objects.all()
    serializer_class = VolumeSerializer


class SutraSet(viewsets.ReadOnlyModelViewSet):
    """
        查看 经API
    """
    queryset = Sutra.objects.all()
    serializer_class = SutraSerializer


class RollSet(viewsets.ReadOnlyModelViewSet):
    """
        查看 卷API
    """
    queryset = Roll.objects.all()
    serializer_class = RollSerializer


class PageSet(viewsets.ReadOnlyModelViewSet):
    """
        查看 页API
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class TranslatorSet(viewsets.ModelViewSet):
    """
    查看, 编辑作译者界面
    """
    queryset = Translator.objects.all()
    serializer_class = TranslatorSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    查看、编辑用户的界面
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    查看、编辑组的界面
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
