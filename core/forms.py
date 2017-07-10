# -*- coding: UTF-8 -*-

__author__ = 'zhaopan'
from django import forms

class ImportTripitakaData(forms.Form):
    seriesInfo = forms.Textarea()
    tripitaka_xls = forms.FileField(required=True)
