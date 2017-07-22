# Register your models here.
from django.contrib import admin

from django.db import models
from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget, ForeignKeyWidget, ManyToManyWidget
from .models import *
from django.db.models.fields import NOT_PROVIDED


class CodeConvertWidget(Widget):
    def __init__(self, prefix_field="", my_prefix="",):
        self.prefix_field = prefix_field
        self.my_prefix = my_prefix
        self._prefix = ""

    def generate_prefix(self, row):
        '''
        生成前缀. 根据
        :param row: 行数据
        :return: 返回生成的前缀
        '''
        if self.prefix_field and row:
            value = self.prefix_field.clean(row)
            if isinstance(self.prefix_field.widget, CacheDuplicateWidget):
                # 如果widget是CacheDuplicateWidget实例, 需要特殊处理下, render时不减去前缀
                value = self.prefix_field.widget.render(value, is_sub=False)
            elif isinstance(self.prefix_field.widget, ForeignKeyWidget):
                # 如果是ForeignKeyWidget, 直接取render的值
                value = self.prefix_field.widget.render(value)
            if value:
                self._prefix = value + self.my_prefix
            else:
                self._prefix = self.my_prefix
            self._prefix_len = len(self._prefix)
        return self._prefix

    def clean(self, value, row=None, *args, **kwargs):
        value = str(value)
        # 如果前缀是空的就生成前缀.
        if not self._prefix:
            self.generate_prefix(row)
        if value and self._prefix and not value.startswith(self._prefix):
            value = self._prefix + value
        return value

    def render(self, value, obj=None):
        if value is None and isinstance(obj, models.Model):
            value = super(CodeConvertWidget, self).render(value, obj)
        value = str(value)
        if value and self._prefix and value.startswith(self._prefix):
            value = value[self._prefix_len:]
        return value

class CacheDuplicateWidget(ForeignKeyWidget):
    cacheMap = {}
    def __init__(self, model, field='pk', prefix_field="", my_prefix="", *args, **kwargs):
        '''
        :param prefix_field: 所依赖的前缀列字段. 这会通过这个字段取出excel中存储的值作为前缀的前缀.
        :param my_prefix: 本widget所在的字段, 自定义加的前缀
        '''
        self.prefix_field = prefix_field
        self.my_prefix = my_prefix
        self._prefix = ""
        super(CacheDuplicateWidget, self).__init__(model, field, *args, **kwargs)

    def generate_prefix(self, row):
        '''
        生成前缀. 根据
        :param row: 行数据
        :return: 返回生成的前缀
        '''
        if self.prefix_field and row:
            value = self.prefix_field.clean(row)
            if isinstance(self.prefix_field.widget, CacheDuplicateWidget):
                # 如果widget是CacheDuplicateWidget实例, 需要特殊处理下, render时不减去前缀
                value = self.prefix_field.widget.render(value, is_sub=False)
            elif isinstance(self.prefix_field.widget, ForeignKeyWidget):
                # 如果是ForeignKeyWidget, 直接取render的值
                value = self.prefix_field.widget.render(value)
            if value:
                self._prefix = value + self.my_prefix
            else:
                self._prefix = self.my_prefix
            self._prefix_len = len(self._prefix)
        return self._prefix

    def clean(self, value, row=None, *args, **kwargs):
        instance = None
        value = str(value)
        # 如果前缀是空的就生成前缀.
        if not self._prefix:
            self.generate_prefix(row)
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

    def render(self, value, obj=None, is_sub=True):
        if isinstance(value, models.Model):
            value = super(CacheDuplicateWidget, self).render(value, obj)
        value = str(value)
        if is_sub and value and self._prefix and value.startswith(self._prefix):
            value = value[self._prefix_len:]
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
    series = fields.Field(
        column_name='series',
        attribute='series',
        widget=MyForeignKeyWidget(Series, 'code'))
    sutra = fields.Field(
        column_name='sutra',
        attribute='sutra',
        widget=MyForeignKeyWidget(Sutra, 'code'))
    sutra__name = fields.Field(
        column_name='sutra__name',
        attribute='sutra__name',
        readonly=False)
    sutra__lqsutra = TwoNestedField(
        nested_field=sutra,
        column_name='sutra__lqsutra',
        attribute='sutra__lqsutra',
        widget=MyForeignKeyWidget(LQSutra, 'code'))
    sutra__lqsutra__name = fields.Field(
        column_name='sutra__lqsutra__name',
        attribute='sutra__lqsutra__name',
        readonly=False)
    code = fields.Field(
        column_name='code',
        attribute='code',
        readonly=False,
        widget=CodeConvertWidget(prefix_field=sutra, my_prefix="_R"))
    start_volume = fields.Field(
        column_name='start_volume',
        attribute='start_volume',
        widget=CacheDuplicateWidget(Volume, 'code', prefix_field=series, my_prefix="_V"))
    end_volume = fields.Field(
        column_name='end_volume',
        attribute='end_volume',
        widget=CacheDuplicateWidget(Volume, 'code', prefix_field=series, my_prefix="_V"))
    start_page = fields.Field(
        column_name='start_page',
        attribute='start_page',
        widget=CacheDuplicateWidget(Page, 'code', prefix_field=start_volume, my_prefix="_P"))
    end_page = fields.Field(
        column_name='end_page',
        attribute='end_page',
        widget=CacheDuplicateWidget(Page, 'code', prefix_field=end_volume, my_prefix="_P"))
    class Meta:
        model = Roll
        import_id_fields = ('code',)
        export_order = ('series', 'sutra', 'sutra__name', 'sutra__lqsutra', 'sutra__lqsutra__name', 'type', 'code', 'start_volume', 'start_page', 'end_page', 'end_volume', 'remark')
        fields = ('series', 'sutra', 'sutra__name', 'sutra__lqsutra', 'sutra__lqsutra__name', 'code', 'type', 'start_volume', 'end_volume', 'start_page', 'end_page', 'remark')

    # def after_import_instance(self, instance, new, **kwargs):
    #     for field in self.get_fields():
    #         if isinstance(field.widget, SutraName):
    #             field.widget._instance = instance

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

    def after_import_row(self, row, row_result, **kwargs):
        # 清除行内字段的前缀, 新的一行需要重新计算
        for field in self.get_fields():
            if isinstance(field.widget, ManyToManyWidget):
                continue
            setattr(field.widget, '_prefix', '')

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
    list_filter = ["series", "sutra", "code", ]
    relfield_style = "fk-select"
    reversion_enable = True
    resource_class = RollRescource

# admin.site.register(LQSutra, LQSutraAdmin)
admin.site.register(Roll, RollAdmin)
admin.site.site_header = '龙泉大藏经'
admin.site.site_title = '龙泉大藏经'
admin.site.index_title = '龙泉大藏经'