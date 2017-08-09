from django.db import models

# Create your models here.

from django.db import models
import uuid
from .utils import ROLL_TYPE_CHOICES, SUTRA_TYPE_CHOICES, get_sutra_type, extract_roll_type, get_roll_type_desc, getLastIntCode, getFirstCharCode, call_delete_instance, get_instance
'''
[Django API](https://docs.djangoproject.com/en/1.11/)
[Django中null和blank的区别](http://www.tuicool.com/articles/2ABJbmj)

Django 数据库访问性能优化
http://www.voidcn.com/blog/permike/article/p-6172184.html
注：django对model中的fk和unique = True的字段将自动创建索引。

Django 优化杂谈
https://zhu327.github.io/2017/04/21/django-%E4%BC%98%E5%8C%96%E6%9D%82%E8%B0%88/
'''

class Series(models.Model):
    SERIES = 'SS'
    OFFPRINT = 'OP'
    TYPE_CHOICES = (
        (SERIES, '藏经丛书'),
        (OFFPRINT, '单行本'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='编号')
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
    code = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='册名')
    series = models.ForeignKey(Series, null=True, blank=True, related_name='volumes', on_delete=models.SET_NULL, verbose_name='版本')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_page = models.CharField(max_length=64, null=True, blank=True, verbose_name="起始页")
    end_page = models.CharField(max_length=64, null=True, blank=True, verbose_name='终止页')
    resource = models.FileField(null=True, blank=True, verbose_name='资源')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def save_by_roll(self, roll=None):
        # 卷是不会跨册的
        if roll:
            self.series = roll.series
            if roll.start_page and roll.end_page:
                if getLastIntCode(roll.start_page) < getLastIntCode(self.start_page, 10000000000):
                    self.start_page = roll.start_page
                if getLastIntCode(roll.end_page) > getLastIntCode(self.end_page, -1):
                    self.end_page = roll.end_page
            self.save()

    def save_by_sutra(self, sutra=None):
        if sutra:
            self.series = sutra.series
            self.save()

    def delete_instance(self, all=False):
        if all:
            call_delete_instance(self.start_page, Page)
            call_delete_instance(self.end_page, Page)
        try:
            Volume.objects.get(id__exact=self.id).delete()
        except Volume.DoesNotExist as e:
            pass

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"册"
        verbose_name_plural = u"册管理"
        ordering = ['name']
        ordering = ('series', 'code')


class Sutra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='经名')
    type = models.CharField(
        db_index=True,
        max_length=2,
        choices=SUTRA_TYPE_CHOICES,
        default='ST',
        verbose_name='类型'
    )
    series = models.ForeignKey(Series, null=True, blank=True, related_name='sutras', on_delete=models.SET_NULL, verbose_name='版本')
    #clazz = models.CharField(max_length=64, null=True, blank=True, verbose_name="部别")
    clazz = models.CharField(max_length=64, null=True, blank=True, verbose_name="部别")
    lqsutra = models.ForeignKey('LQSutra', null=True, blank=True, related_name='lqsutra_list', on_delete=models.SET_NULL, verbose_name='龙泉收录')
    translator = models.ForeignKey('Translator', null=True, blank=True, verbose_name='作译者')
    dynasty = models.CharField(max_length=64, null=True, blank=True, verbose_name="朝代")
    historic_site = models.CharField(max_length=64, null=True, blank=True, verbose_name="译经地点")
    roll_count = models.IntegerField(null=True, blank=True, verbose_name='卷数')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_volume = models.CharField(max_length=64, null=True, blank=True, verbose_name="起始册")
    end_volume = models.CharField(max_length=64, null=True, blank=True, verbose_name="终止册")
    start_page = models.CharField(max_length=64, null=True, blank=True, verbose_name="起始页")
    end_page = models.CharField(max_length=64, null=True, blank=True, verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, null=True, blank=True, verbose_name='千字文')
    resource = models.FileField(null=True, blank=True, verbose_name='资源')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def before_save(self):
        self.type = get_sutra_type(self.remark)
        if self.series is None:
            code = getFirstCharCode(self.code)
            if code:
                instance = get_instance(Series, 'code', code, create_no_exist=True, save_no_exist=True)
                self.series = instance

        # 如果lqsutra_code为空或者根据它没有找到相应的龙泉经目信息, 就置为空.
        if self.lqsutra and not self.lqsutra.name:
            self._lqsutra = self.lqsutra
            self.lqsutra = None

        if self.start_volume:
            instance = get_instance(Volume, 'code', self.start_volume)
            if instance:
                instance.save_by_sutra(self)
        if self.end_volume:
            instance = get_instance(Volume, 'code', self.end_volume)
            if instance:
                instance.save_by_sutra(self)

    def after_save(self):
        if hasattr(self, '_lqsutra'):
            self.lqsutra = self._lqsutra

    def save_by_roll(self, roll=None):
        if roll:
            # 如果经的版本信息没有, 需要找到.并关联上, 这可能是一条新的记录, 所以没有
            if self.series is None:
                code = getFirstCharCode(self.code)
                if code:
                    instance = get_instance(Series, 'code', code, create_no_exist=True, save_no_exist=True)
                    self.series = instance

            if getLastIntCode(roll.start_volume) <= getLastIntCode(self.start_volume, 1000000):
                self.start_volume = roll.start_volume
                if getLastIntCode(roll.start_page) < getLastIntCode(self.start_page, 10000000):
                    self.start_page = roll.start_page

            if getLastIntCode(roll.end_volume) >= getLastIntCode(self.end_volume):
                self.end_volume = roll.end_volume
                if getLastIntCode(roll.end_page) > getLastIntCode(self.end_page):
                    self.end_page = roll.end_page

            # 如果lqsutra_code为空或者根据它没有找到相应的龙泉经目信息, 就置为空.
            if self.lqsutra and not self.lqsutra.name:
                self._lqsutra = self.lqsutra
                self.lqsutra = None
            # 保存经
            self.save()
            if hasattr(self, '_lqsutra'):
                self.lqsutra = self._lqsutra

    def before_delete(self, all=False):
        if all:
            # call_delete_instance(self.start_page, Page)
            # call_delete_instance(self.end_page, Page)
            # 需要做下起始册到结束册的删除 ****
            call_delete_instance(self.start_volume, Volume)
            call_delete_instance(self.end_volume, Volume)
            list = self.rolls.all()
            for roll in list:
                roll.before_delete(all)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"经"
        verbose_name_plural = u"经管理"
        ordering = ('series', 'code')


class Roll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='卷名')
    type = models.CharField(
        db_index=True,
        max_length=16,
        choices=ROLL_TYPE_CHOICES,
        default='roll',
        verbose_name='类型'
    )
    series = models.ForeignKey(Series, null=True, blank=True, related_name='rolls', on_delete=models.SET_NULL, verbose_name='版本')
    sutra = models.ForeignKey(Sutra, null=True, blank=True, related_name='rolls', on_delete=models.SET_NULL, verbose_name='经')
    page_count = models.IntegerField(null=True, blank=True, verbose_name='页数')
    start_volume = models.CharField(max_length=64, null=True, blank=True, verbose_name="起始册")
    end_volume = models.CharField(max_length=64, null=True, blank=True, verbose_name="终止册")
    start_page = models.CharField(max_length=64, null=True, blank=True, verbose_name="起始页")
    end_page = models.CharField(max_length=64, null=True, blank=True, verbose_name='终止页')
    qianziwen = models.CharField(max_length=8, null=True, blank=True, verbose_name='千字文')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def before_save(self):
        code = str(getLastIntCode(self.code))
        if code == '0':
            self.type = extract_roll_type(self.code)
            self.name = get_roll_type_desc(self.type)
        else:
            self.name = code
            # self.type = roll_type(self.code) #默认卷

        if self.sutra:
            self.sutra.save_by_roll(self)
            self.series = self.sutra.series

        if self.start_volume:
            instance = get_instance(Volume, 'code', self.start_volume)
            if instance:
                instance.save_by_roll(self)
        if self.end_volume:
            instance = get_instance(Volume, 'code', self.end_volume)
            if instance:
                instance.save_by_roll(self)

    def after_save(self):
        if self.start_page:
            instance = get_instance(Page, 'code', self.start_page)
            if instance:
                instance.save_by_roll(self)
        if self.end_page:
            instance = get_instance(Page, 'code', self.end_page)
            if instance:
                instance.save_by_roll(self)

    def before_delete(self, all=False):
        if all:
            # call_delete_instance(self.start_page, Page)
            # call_delete_instance(self.end_page, Page)
            list = self.pages.all()
            for page in list:
                page.delete_instance(all)

    def __str__(self):
        return self.code

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
    code = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='编号')
    name = models.CharField(max_length=64, verbose_name='页码')
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=CONTENT,
        verbose_name='类型'
    )
    # series = models.ForeignKey(Series, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='部')
    # volume = models.ForeignKey(Volume, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='册')
    # sutra = models.ForeignKey(Sutra, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='经')
    roll = models.ForeignKey(Roll, null=True, blank=True, related_name='pages', on_delete=models.SET_NULL, verbose_name='卷')
    # roll = models.CharField(max_length=64, null=True, blank=True, verbose_name='卷')
    series = models.CharField(max_length=64, null=True, blank=True, db_index=True, verbose_name='部')
    volume = models.CharField(max_length=64, null=True, blank=True, db_index=True, verbose_name='册')
    sutra = models.CharField(max_length=64, null=True, blank=True, db_index=True, verbose_name='经')
    pre_page = models.CharField(max_length=64, null=True, blank=True, verbose_name='上一页')
    next_page = models.CharField(max_length=64, null=True, blank=True, verbose_name='下一页')

    def save_by_roll(self, roll):
        self.name = getLastIntCode(self.code)
        self.roll = roll
        self.volume = roll.start_volume
        self.sutra = roll.sutra.code
        self.series = roll.series.code if roll.series else ''
        self.save()

    def delete_instance(self, all=False):
        if all:
            # 这里可以删除页相关的资源
            pass
        try:
            Page.objects.get(id__exact=self.id).delete()
            # self.delete()
        except Page.DoesNotExist as e:
            pass

    def __str__(self):
        return self.code

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
    #foreign_code = models.CharField(max_length=64, unique=True, db_index=True,  verbose_name='资源来源')
    page = models.ForeignKey(Page, related_name='page_resources', on_delete=models.CASCADE, verbose_name='页')
    type = models.CharField(
        db_index=True,
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
        db_index=True,
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
    name = models.CharField(max_length=256, db_index=True, verbose_name='作译者名字')
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True, db_index=True, verbose_name='龙泉编码')
    name = models.CharField(max_length=256, db_index=True, verbose_name='龙泉经名')
    translator = models.ForeignKey('Translator', null=True, blank=True, verbose_name='作译者')
    roll_count = models.IntegerField(null=True, blank=True, verbose_name='卷数')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')

    def before_save(self):
        if self.translator:
            self.translator.save()

    def after_save(self):
        pass

    def before_delete(self, all=False):
        if all:
            # 额外相关的删除
            pass
        # try:
        #     LQSutra.objects.get(id__exact=self.id).delete()
        # except LQSutra.DoesNotExist as e:
        #     pass

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
    name = models.CharField(max_length=64, db_index=True, verbose_name='标准名')
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
    name = models.CharField(max_length=64, db_index=True, verbose_name='名字')
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
