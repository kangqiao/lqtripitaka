from django.db import models

# Create your models here.

from django.db import models


class Translator(models.Model):
    TRANSLATOR = 'TS'
    AUTHOR = 'AH'
    TYPE_CHOICES = (
        (TRANSLATOR, 'Translator'),
        (AUTHOR, 'author'),
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=TRANSLATOR
    )
    name = models.CharField(max_length=64, blank=True, default='')
    nameA = models.CharField(max_length=64, blank=True, default='')
    nameB = models.CharField(max_length=64, blank=True, default='')
    remark = models.CharField(max_length=128, blank=True)
