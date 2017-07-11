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
    roll_count = models.IntegerField(null=True, blank=True, verbose_name='卷数')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    word_count = models.IntegerField(null=True, blank=True, verbose_name='字数')
    dynasty = models.CharField(max_length=64, null=True, blank=True, verbose_name="刊刻时间")
    historic_site = models.CharField(max_length=64, null=True, blank=True, verbose_name="刊刻地点")
    library_site = models.CharField(max_length=64, null=True, blank=True, verbose_name="馆藏地")
    book_reservation = models.CharField(max_length=64, null=True, blank=True, verbose_name="典藏号")
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
        ordering = ('code', 'type')


class Volume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='册名')
    series = models.ForeignKey(Series, null=True, blank=True, related_name='volumes', on_delete=models.SET_NULL, verbose_name='版本')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_page = models.UUIDField(null=True, blank=True, verbose_name="起始页")
    end_page = models.UUIDField(null=True, blank=True, verbose_name='终止页')
    resource = models.FileField(null=True, blank=True, verbose_name='资源')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"册"
        verbose_name_plural = u"册管理"
        ordering = ['name']
        ordering = ('series', 'code')


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
    #clazz = models.CharField(max_length=64, null=True, blank=True, verbose_name="部别")
    clazz = models.CharField(max_length=64, null=True, blank=True, verbose_name="部别")
    lqsutra = models.ForeignKey('lqSutra', null=True, blank=True, related_name='lqsutra_list', on_delete=models.SET_NULL, verbose_name='龙泉收录')
    translator = models.ForeignKey('Translator', null=True, blank=True, verbose_name='作译者')
    dynasty = models.CharField(max_length=64, null=True, blank=True, verbose_name="朝代")
    historic_site = models.CharField(max_length=64, null=True, blank=True, verbose_name="译经地点")
    roll_count = models.IntegerField(null=True, blank=True, verbose_name='卷数')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_volume = models.UUIDField(null=True, blank=True, verbose_name="起始册")
    end_volume = models.UUIDField(null=True, blank=True, verbose_name="终止册")
    start_page = models.UUIDField(null=True, blank=True, verbose_name="起始页")
    end_page = models.UUIDField(null=True, blank=True, verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, null=True, blank=True, verbose_name='千字文')
    resource = models.FileField(null=True, blank=True, verbose_name='资源')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"经"
        verbose_name_plural = u"经管理"
        ordering = ('series', 'code')


class Roll(models.Model):
    TYPE_CHOICES = (
        ('roll', '卷'),
        ('preface', '序'),
        ('all_preface', '总序'),
        ('origin_preface', '原序'),
        ('catalogue', '总目'),
        ('postscript', '跋'),
        ('corrigenda', "勘误表")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='卷名')
    type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        default='roll',
        verbose_name='类型'
    )
    series = models.ForeignKey(Series, null=True, blank=True, related_name='rolls', on_delete=models.SET_NULL, verbose_name='版本')
    sutra = models.ForeignKey(Sutra, null=True, blank=True, related_name='rolls', on_delete=models.SET_NULL, verbose_name='经')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_volume = models.UUIDField(null=True, blank=True, verbose_name="起始册")
    end_volume = models.UUIDField(null=True, blank=True, verbose_name="终止册")
    start_page = models.UUIDField(null=True, blank=True, verbose_name="起始页")
    end_page = models.UUIDField(null=True, blank=True, verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, null=True, blank=True, verbose_name='千字文')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"卷"
        verbose_name_plural = u"卷管理"
        ordering = ('sutra', 'code')


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
        ordering = ('sutra', 'code')


class PageResource(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    INSET = 'inset'
    PDF = 'pdf'
    TYPE_CHOICES = (
        (TEXT, '文本'),
        (IMAGE, '图片'),
        (INSET, '插图'),
        (PDF, 'PDF'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #foreign_code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='资源来源')
    page = models.ForeignKey(Page, related_name='page_resources', on_delete=models.CASCADE, verbose_name='页')
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=IMAGE,
        verbose_name='类型'
    )
    CBEAT = 'cbeat'
    HANDWORK = 'hand'
    NETWORK = "net"
    SOURCE_CHOICES = (
        (CBEAT, 'cbeta采集'),
        (HANDWORK, '手工录入'),
        (NETWORK, '网络采集'),
    )
    source = models.CharField(
        max_length=8,
        choices=SOURCE_CHOICES,
        default=HANDWORK,
        verbose_name='来源'
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

class LQSutra(models.Model):
    code = models.CharField(max_length=64, unique=True, blank=True, verbose_name='龙泉编码')
    name = models.CharField(max_length=64, verbose_name='龙泉经名')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = u"龙泉经录"
        verbose_name_plural = u"龙泉收录管理"

SERIES = 'series'
SUTRA = 'sutra'
DYNASTY = 'dynasty'
HISTORIC_SITE = "site"
TRANSLATOR = "trans"
NORM_TYPE_CHOICES = (
    (SERIES, '标准版本名'),
    (SUTRA, '标准经名'),
    (DYNASTY, '标准朝代'),
    (HISTORIC_SITE, '标准地名'),
    (TRANSLATOR, '标准作译者'),
)

class NormName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, verbose_name='标准名')
    type = models.CharField(
        max_length=8,
        choices=NORM_TYPE_CHOICES,
        default=SUTRA,
        verbose_name='标准类型'
    )
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"标准名"
        verbose_name_plural = u"标准名管理"

class NormNameMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=8,
        choices=NORM_TYPE_CHOICES,
        default=SUTRA,
        verbose_name='标准类型'
    )
    name = models.CharField(max_length=64, verbose_name='名字')
    norm_name = models.ForeignKey(NormName, related_name='map_list', on_delete=models.CASCADE, verbose_name='隶属标准名')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"标准名关联"
        verbose_name_plural = u"名称对照管理"


class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"访问记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s Access Record" % self.date.strftime('%Y-%m-%d')
