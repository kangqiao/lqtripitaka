from django.db import models

# Create your models here.

from django.db import models
import uuid

'''
[Django API](https://docs.djangoproject.com/en/1.11/)
[Django中null和blank的区别](http://www.tuicool.com/articles/2ABJbmj)
'''


class Series(models.Model):
    SERIES = 'SS'
    OFFPRINT = 'OP'
    TYPE_CHOICES = (
        (SERIES, '藏经丛书'),
        (OFFPRINT, '单行本'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='版本名')
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=SERIES,
        verbose_name='版本类型'
    )
    volume_count = models.IntegerField(null=True, blank=True, verbose_name="册数")
    sutra_count = models.IntegerField(null=True, blank=True, verbose_name="经数")
    dynasty = models.CharField(max_length=64, null=True, blank=True, verbose_name="朝代")
    historic_site = models.CharField(max_length=64, null=True, blank=True, verbose_name="刻经地点")
    publish_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="出版社")
    publish_date = models.DateField(null=True, blank=True, verbose_name="出版时间")
    publish_edition = models.SmallIntegerField(null=True, blank=True, verbose_name="版次")
    publish_prints = models.SmallIntegerField(null=True, blank=True, verbose_name="印次")
    publish_ISBN = models.CharField(max_length=64, null=True, blank=True, verbose_name="ISBN")
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"藏经版本"
        verbose_name_plural = u"藏经版本管理"


class Volume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='册名')
    series = models.ForeignKey(Series, null=True, blank=True, related_name='volumes', on_delete=models.SET_NULL, verbose_name='版本')
    start_page = models.UUIDField(null=True, blank=True, verbose_name="起始页")
    end_page = models.UUIDField(null=True, blank=True, verbose_name='终止页')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"册"
        verbose_name_plural = u"册管理"
        ordering = ['name']


class Sutra(models.Model):
    SUTTA = 'ST'
    RESTRAIN = 'RT'
    TREATISE = 'TT'
    TYPE_CHOICES = (
        (SUTTA, '经'),
        (RESTRAIN, '律'),
        (TREATISE, '论'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='经名')
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=SUTTA,
        verbose_name='类型'
    )
    series = models.ForeignKey(Series, null=True, blank=True, related_name='sutras', on_delete=models.SET_NULL, verbose_name='版本')
    clazz = models.CharField(max_length=64, null=True, blank=True, verbose_name="部别")
    translator = models.ForeignKey('Translator', null=True, blank=True, verbose_name='作译者')
    dynasty = models.CharField(max_length=64, null=True, blank=True, verbose_name="朝代")
    historic_site = models.CharField(max_length=64, null=True, blank=True, verbose_name="译经地点")
    roll_count = models.IntegerField(null=True, blank=True, verbose_name='卷数')
    start_page = models.UUIDField(null=True, blank=True, verbose_name="起始页")
    end_page = models.UUIDField(null=True, blank=True, verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, null=True, blank=True, verbose_name='千字文')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"经"
        verbose_name_plural = u"经管理"
        ordering = ['name']


class Roll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='卷名')
    series = models.ForeignKey(Series, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='版本')
    sutra = models.ForeignKey(Sutra, null=True, blank=True, related_name='rolls', on_delete=models.SET_NULL, verbose_name='经')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_page = models.UUIDField(null=True, blank=True, verbose_name="起始页")
    end_page = models.UUIDField(null=True, blank=True, verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, null=True, blank=True, verbose_name='千字文')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"卷"
        verbose_name_plural = u"卷管理"
        ordering = ['name']


class Page(models.Model):
    COVER = 'cover'
    PROLOGUE = 'prologue'
    PREFACE = 'Preface'
    CATALOG = 'catalog'
    PUBLISH = 'publish'
    BLANK = 'blank'
    CONTENT = 'content'
    TYPE_CHOICES = (
        (COVER, '封面'),
        (PROLOGUE, '序言'),
        (PREFACE, '前言'),
        (CATALOG, '目录'),
        (PUBLISH, '出版页'),
        (BLANK, '空白页'),
        (CONTENT, '内容'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='页码')
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=CONTENT,
        verbose_name='类型'
    )
    series = models.ForeignKey(Series, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='部')
    volume = models.ForeignKey(Volume, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='册')
    sutra = models.ForeignKey(Sutra, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='经')
    roll = models.ForeignKey(Roll, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='卷')
    pre_page = models.UUIDField(null=True, blank=True, verbose_name='上一页')
    next_page = models.UUIDField(null=True, blank=True, verbose_name='下一页')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"页"
        verbose_name_plural = u"页管理"
        ordering = ['name']


class PageResource(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    INSET = 'inset'
    TYPE_CHOICES = (
        (TEXT, '文本'),
        (IMAGE, '图片'),
        (INSET, '插图'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(Page, related_name='page_resources', on_delete=models.CASCADE, verbose_name='页')
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=IMAGE,
        verbose_name='类型'
    )
    resource = models.FileField(verbose_name='资源')

    def __str__(self):
        typeName = ""
        for item in self.TYPE_CHOICES:
            if self.type == item[0]:
                typeName = item[1]
        return typeName + " => " + self.resource.name

    class Meta:
        verbose_name = u"页资源"
        verbose_name_plural = u"页资源列表"


class Translator(models.Model):
    TRANSLATOR = 'TS'
    AUTHOR = 'AH'
    TYPE_CHOICES = (
        (TRANSLATOR, '译者'),
        (AUTHOR, '作者'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, verbose_name='作译者名字')
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=TRANSLATOR,
        verbose_name='类型'
    )
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"作译者"
        verbose_name_plural = u"作译者管理"


class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"访问记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s Access Record" % self.date.strftime('%Y-%m-%d')
