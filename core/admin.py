# Register your models here.
from django.contrib import admin

from django.db import models
from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget, ForeignKeyWidget, ManyToManyWidget
from .models import *
from django.db.models.fields import NOT_PROVIDED

class LineNumWidget(Widget):
    def __init__(self):
        self._line_num = None
    def clean(self, value, row=None, *args, **kwargs):
        if self._line_num != value:
            self._line_num = value
        return self._line_num

    def render(self, value, obj=None):
        return self._line_num

class CodeConvertWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        value = str(value)
        if value and self._prefix and not value.startswith(self._prefix):
            value = self._prefix + value
        return value

    def render(self, value, obj=None):
        value = str(value)
        if value and self._prefix and value.startswith(self._prefix):
            value = value[len(self._prefix):]
        return value

class CacheDuplicateWidget(ForeignKeyWidget):
    cacheMap = {}
    def clean(self, value, row=None, *args, **kwargs):
        instance = None
        value = str(value)
        if value and self._prefix and not value.startswith(self._prefix):
            value = self._prefix + value
        try:
            instance = super(CacheDuplicateWidget, self).clean(value, row)
        except Exception as e:
            pass
        if not instance:
            if value in CacheDuplicateWidget.cacheMap:
                instance = CacheDuplicateWidget.cacheMap.get(value)
            else:
                instance = self.model()
                setattr(instance, self.field, value)
                CacheDuplicateWidget.cacheMap[value] = instance
        return instance
    def render(self, value, obj=None):
        value = str(value)
        m = self._prefix_re.search(value) if self._prefix_re else None
        value = m.group('value') if m else value
        return value

class MyForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        instance = None
        try:
            instance = super(MyForeignKeyWidget, self).clean(value, row)
        except Exception as e:
            pass
        if not instance:
            instance = self.model()
            setattr(instance, self.field, value)
        return instance

class TwoNestedField(fields.Field):
    def __init__(self, nested_field, attribute=None, column_name=None, widget=None,
                 default=NOT_PROVIDED, readonly=False):
        self.nested_field = nested_field
        super(TwoNestedField, self).__init__(attribute, column_name, widget, default, readonly)

    def save(self, obj, data):
        if not self.nested_field.readonly:
            obj = self.nested_field.get_value(obj)
            if obj and not self.readonly:
                attrs = self.attribute.split('__')
                setattr(obj, attrs[-1], self.clean(data))

class RollRescource(ModelResource):
    line_num = fields.Field(
        column_name=u'行号',
        attribute='line_num',
        readonly=False,
        widget=LineNumWidget())
    sutra = fields.Field(
        column_name=u'经号',
        attribute='sutra',
        widget=MyForeignKeyWidget(Sutra, 'code'))
    sutra__name = fields.Field(
        column_name=u'经名',
        attribute='sutra__name',
        readonly=False)
    sutra__lqsutra = TwoNestedField(
        nested_field=sutra,
        column_name=u'龙泉收录',
        attribute='sutra__lqsutra',
        widget=MyForeignKeyWidget(LQSutra, 'code'))
    code = fields.Field(
        column_name=u'卷号',
        attribute='code',
        readonly=False,
        widget=CodeConvertWidget())
    start_volume = fields.Field(
        column_name=u'起始册',
        attribute='start_volume',
        widget=CacheDuplicateWidget(Volume, 'code'))
    end_volume = fields.Field(
        column_name=u'结束册',
        attribute='end_volume',
        widget=CacheDuplicateWidget(Volume, 'code'))
    start_page = fields.Field(
        column_name=u'起始页',
        attribute='start_page',
        widget=CacheDuplicateWidget(Page, 'code'))
    end_page = fields.Field(
        column_name=u'结束页',
        attribute='end_page',
        widget=CacheDuplicateWidget(Page, 'code'))
    remark = fields.Field(
        column_name=u'备注',
        attribute='remark',
        readonly=False)
    class Meta:
        model = Roll
        import_id_fields = ('code',)
        export_order = ('line_num', 'sutra', 'sutra__name', 'sutra__lqsutra', 'code', 'start_volume', 'start_page', 'end_page', 'end_volume', 'remark')
        fields = ('line_num', 'sutra', 'sutra__name', 'sutra__lqsutra', 'code', 'start_volume', 'end_volume', 'start_page', 'end_page', 'remark')

    def __init__(self):
        self._line_num = 0
        self.preface_re = re.compile(r'(?P<preface>序|总序|原序|总目|跋|勘误表)', re.M)

    def before_import_row(self, row, **kwargs):
        # 根据row为每个字段生成前缀
        self._line_num = self._line_num + 1
        row[self.fields['line_num'].column_name] = self._line_num
        sutra_code = row[self.fields['sutra'].column_name]
        series_re = re.findall(r'^([a-zA-Z]+)\d+', sutra_code)
        series_code = series_re[0] if series_re else ''
        # 卷的前缀
        self.fields['code'].widget._prefix = sutra_code + '_R'
        re_roll_prefix = re.compile(r'^(?P<series>' + series_code + ')_R(?P<value>\d+)$', re.I)
        self.fields['code'].widget._prefix_re = re_roll_prefix
        code = str(row[self.fields['code'].column_name])
        if code == "0":
            remark = str(row[self.fields['remark'].column_name])
            m = self.preface_re.search(remark)
            name = m.group("preface") if m else ""
        # 册的前缀
        volume_prefix = series_code + '_V'
        self.fields['start_volume'].widget._prefix = volume_prefix
        self.fields['end_volume'].widget._prefix = volume_prefix
        re_volume_prefix = re.compile(r'^(?P<series>' + series_code + ')_V(?P<value>\d+)$', re.I)
        self.fields['start_volume'].widget._prefix_re = re_volume_prefix
        self.fields['end_volume'].widget._prefix_re = re_volume_prefix
        # 页的前缀
        self.fields['start_page'].widget._prefix = volume_prefix + str(row[self.fields['start_volume'].column_name]) + '_P'
        self.fields['end_page'].widget._prefix = volume_prefix + str(row[self.fields['end_volume'].column_name]) + '_P'
        re_page_prefix = re.compile(r'^(?P<series>' + series_code + ')_V(?P<volume>\d+)_P(?P<value>\d+)$', re.I)
        self.fields['start_page'].widget._prefix_re = re_page_prefix
        self.fields['end_page'].widget._prefix_re = re_page_prefix

    def for_delete(self, row, instance):
        value = row[u'操作']
        if value and (value == u'删除' or value.lower() == 'delete' or value.lower() == 'del'):
            if instance:
                try:
                    Roll.objects.get(id__exact=instance.id).delete()
                except Roll.DoesNotExist as e:
                    pass
            return True
        elif value and (value == u'跳过' or value.lower() == 'skip'):
            return True
        return False

    def before_save_instance(self, instance, using_transactions, dry_run):
        if not using_transactions and dry_run:
            pass
        else:
            instance.before_save()

    def after_save_instance(self, instance, using_transactions, dry_run):
        if not using_transactions and dry_run:
            pass
        else:
            instance.after_save()

    # def after_import_row(self, row, row_result, **kwargs):
    #     # 清除行内字段的前缀, 新的一行需要重新计算
    #     for field in self.get_fields():
    #         if isinstance(field.widget, ManyToManyWidget):
    #             continue
    #         setattr(field.widget, '_prefix', '')

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if using_transactions:
            if dry_run or result.has_errors():
                pass
            else:
                #此处可做一些数据的统计, 例如新增多少, 更新多少,
                #还有, 对此次导入的卷数, 册数, 经数, 页数, 以及初始化所有页基础数据.
                pass


class RollAdmin(ImportMixin, admin.ModelAdmin):
    def real_page_count(self, instance):
        count = Page.objects.filter(roll=instance.id).count()
        if count > 0:
            return """<a href='/xadmin/core/page/?_p_roll__id__exact=%s'>%s</a>""" % (instance.id, count)
        return count
    real_page_count.short_description = "实存页数"
    real_page_count.allow_tags = True
    real_page_count.is_column = True

    list_display = ("series", "sutra", "code", "type", "name", "start_volume", "start_page", "end_page",  "end_volume", "real_page_count", "remark")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name"]
    #list_filter = ["series", "sutra", "code", ]
    relfield_style = "fk-select"
    reversion_enable = True
    resource_class = RollRescource

class LQSutraRescource(ModelResource):
    line_num = fields.Field(
        column_name=u'行号',
        attribute='line_num',
        readonly=False,
        widget=LineNumWidget())
    code = fields.Field(
        column_name=u'龙泉编码',
        attribute='code',
        readonly=False,
        widget=CodeConvertWidget())
    name = fields.Field(
        column_name=u'实体经名',
        attribute='name',
        readonly=False)
    translator = fields.Field(
        column_name=u'作译者',
        attribute='translator',
        widget=MyForeignKeyWidget(Translator, 'name'))
    roll_count = fields.Field(
        column_name=u'总卷数',
        attribute='roll_count',
        readonly=False)
    remark = fields.Field(
        column_name=u'备注',
        attribute='remark',
        readonly=False)
    class Meta:
        model = LQSutra
        import_id_fields = ('code',)
        export_order = ('line_num', "code", "name", "translator", "roll_count", "remark")
        fields = ('line_num', "code", "name", "translator", "roll_count", "remark")

    def __init__(self):
        self._line_num = 0
        self.preface_re = re.compile(r'(?P<preface>序|总序|原序|总目|跋|勘误表)', re.M)

    def for_delete(self, row, instance):
        value = row[u'操作']
        if value and (value == u'删除' or value.lower() == 'delete' or value.lower() == 'del'):
            if instance:
                try:
                    LQSutra.objects.get(id__exact=instance.id).delete()
                except LQSutra.DoesNotExist as e:
                    pass
            return True
        elif value and (value == u'跳过' or value.lower() == 'skip'):
            return True
        return False

    def before_import_row(self, row, **kwargs):
        # 根据row为每个字段生成前缀
        self._line_num = self._line_num + 1
        row[self.fields['line_num'].column_name] = self._line_num
        # 卷的前缀
        self.fields['code'].widget._prefix = 'LQ'

    def before_save_instance(self, instance, using_transactions, dry_run):
        if not using_transactions and dry_run:
            pass
        else:
            instance.before_save()

class LQSutraAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ("code", "name", "translator", "roll_count", "remark")
    list_display_links = ("code", "name",)
    search_fields = ["code", "name"]
    #list_filter = ["code", "name", "translator", ]
    relfield_style = "fk-select"
    reversion_enable = True
    resource_class = LQSutraRescource

admin.site.register(Roll, RollAdmin)
admin.site.register(LQSutra, LQSutraAdmin)
admin.site.site_header = '龙泉大藏经'
admin.site.site_title = '龙泉大藏经'
admin.site.index_title = '龙泉大藏经'