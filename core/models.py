from django.db import models

# Create your models here.

from django.db import models

class Translator(models.Model):
    TRANSLATOR = 'TS'
    AUTHOR = 'AH'
    TYPE_CHOICES = (
        (TRANSLATOR, '译者'),
        (AUTHOR, '作者'),
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=TRANSLATOR,
        verbose_name='类型'
    )
    name = models.CharField(max_length=64, verbose_name='作译者名字')
    nameA = models.CharField(max_length=64, verbose_name='名字A')
    nameB = models.CharField(max_length=64, verbose_name='名字B')
    remark = models.TextField(blank=True, verbose_name='备注')



class Page(models.Model):
    name = models.CharField(max_length=64, verbose_name='页码')
    series = models.ForeignKey('Series', verbose_name='部')
    volume = models.ForeignKey('Volume', verbose_name='册')
    sutra = models.ForeignKey('Sutra', verbose_name='经')
    roll = models.ForeignKey('Roll', verbose_name='卷')
    pre_page = models.ForeignKey('Page', verbose_name='上一页')
    next_page = models.ForeignKey('Page', verbose_name='下一页')
    resource = models.CharField(max_length=128, verbose_name='资源')

class Series(models.Model):
    SERIES = 'SS'
    OFFPRINT = 'OP'
    TYPE_CHOICES = (
        (SERIES, '藏经丛书'),
        (OFFPRINT, '单行本'),
    )
    name = models.CharField(max_length=64, verbose_name='版本名')
    dynasty = models.CharField(max_length=64, verbose_name="朝代")
    historic_site = models.CharField(max_length=64, verbose_name="刻经地点")
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=SERIES,
        verbose_name='版本类型'
    )
    volume_count = models.IntegerField(verbose_name="册数")
    sutra_count = models.IntegerField(verbose_name="经数")
    publish_name = models.CharField(max_length=64, verbose_name="出版社")
    publish_date = models.DateField(auto_now=True, verbose_name="出版时间")
    publish_edition = models.SmallIntegerField(verbose_name="版次")
    publish_prints = models.SmallIntegerField(verbose_name="印次")
    publish_ISBN = models.CharField(max_length=64, verbose_name="ISBN")
    remark = models.TextField(verbose_name='备注')


class Volume(models.Model):
    name = models.CharField(max_length=64, verbose_name='册名')
    series = models.ForeignKey(Series, verbose_name='版本')
    start_page = models.ForeignKey('Page', verbose_name="起始页")
    end_page = models.ForeignKey('Page', verbose_name='终止页')
    remark = models.TextField(verbose_name='备注')
    # 册PDF文件


class Sutra(models.Model):
    SUTTA = 'ST'
    RESTRAIN = 'RT'
    TREATISE = 'TT'
    TYPE_CHOICES = (
        (SUTTA, '经'),
        (RESTRAIN, '律'),
        (TREATISE, '论'),
    )
    name = models.CharField(max_length=64, verbose_name='经名')
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=SUTTA,
        verbose_name='类型'
    )
    series = models.ForeignKey(Series, verbose_name='版本')
    translator = models.ForeignKey(Translator, verbose_name='作译者')
    dynasty = models.CharField(max_length=64, verbose_name="朝代")
    historic_site = models.CharField(max_length=64, verbose_name="刻经地点")
    roll_count = models.IntegerField(verbose_name='卷数')
    start_page = models.ForeignKey('Page', verbose_name="起始页")
    end_page = models.ForeignKey('Page', verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, verbose_name='千字文')
    remark = models.TextField(verbose_name='备注')
    # 册PDF文件


class Roll(models.Model):
    name = models.CharField(max_length=64, verbose_name='卷名')
    sutra = models.ForeignKey(Sutra, verbose_name='经')
    page_count = models.IntegerField(verbose_name='页数')
    start_page = models.ForeignKey('Page', verbose_name="起始页")
    end_page = models.ForeignKey('Page', verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, verbose_name='千字文')
    remark = models.TextField(verbose_name='备注')
