# Register your models here.
from django.contrib import admin

from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import fields
from import_export.widgets import Widget, ForeignKeyWidget
from .models import *
from django.db.models.fields import NOT_PROVIDED


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

class CacheDuplicateWidget(ForeignKeyWidget):
    cacheMap = {}
    def clean(self, value, row=None, *args, **kwargs):
        instance = None
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
        return value

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
    start_volume = fields.Field(
        column_name='start_volume',
        attribute='start_volume',
        widget=CacheDuplicateWidget(Volume, 'code'))
    end_volume = fields.Field(
        column_name='end_volume',
        attribute='end_volume',
        widget=CacheDuplicateWidget(Volume, 'code'))
    start_page = fields.Field(
        column_name='start_page',
        attribute='start_page',
        widget=CacheDuplicateWidget(Page, 'code'))
    end_page = fields.Field(
        column_name='end_page',
        attribute='end_page',
        widget=CacheDuplicateWidget(Page, 'code'))
    class Meta:
        model = Roll
        import_id_fields = ('code',)
        export_order = ('series', 'sutra', 'sutra__name', 'sutra__lqsutra', 'sutra__lqsutra__name', 'type', 'code', 'start_volume', 'start_page', 'end_page', 'end_volume', 'remark')
        fields = ('series', 'sutra', 'sutra__name', 'sutra__lqsutra', 'sutra__lqsutra__name', 'code', 'type', 'start_volume', 'end_volume', 'start_page', 'end_page', 'remark')

    def before_import_row(self, row, **kwargs):
        # 根据row为每个字段生成前缀
        series_code = row[self.fields['series'].column_name]
        sutra_code = row[self.fields['sutra'].column_name]
        # 卷的前缀
        self.fields['code'].widget._prefix = sutra_code + '_R'
        # 册的前缀
        volume_prefix = series_code + '_V'
        self.fields['start_volume'].widget._prefix = volume_prefix
        self.fields['end_volume'].widget._prefix = volume_prefix
        # 页的前缀
        self.fields['start_page'].widget._prefix = volume_prefix + str(row[self.fields['start_volume'].column_name]) + '_P'
        self.fields['end_page'].widget._prefix = volume_prefix + str(row[self.fields['end_volume'].column_name]) + '_P'


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